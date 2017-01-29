import os
import re
import tarfile
import tempfile

from django.utils.translation import ugettext as _
from debian.debian_support import BaseVersion as _BaseVersion


class BaseVersion(_BaseVersion):
    def __init__(self):
        pass

    def _compare(self, other):
        def cmp_part(a, b):
            """ Compare a part of a full Debian version string. """

            def normalize(ver_str):
                """ Pull apart a Debian version fragment into a series of
                    either numeric or non-integer tokens.  For numeric tokens,
                    those are then converted into actual integers.
                """
                # Deal with optional parts.
                ver_str = "0" if not ver_str else ver_str
                return [int(part) if part.isdigit() else part for part in re.findall(r"[^\d]+|\d+", ver_str)]

            # Magical Debian character sort order and the less magical lambda
            # that uses it to generate the custom sort order.
            # Delete is not a valid character in Debian versions, thus it is
            # perfect for padding strings of different lengths when comparing
            # version fragments that have tilde characters.
            order = '~\x7f:' \
                    '0123456789' \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                    'abcdefghijklmnopqrstuvwxyz' \
                    '-+.'
            key = lambda word: [order.index(c) for c in word]

            # Tokenize and backfill the values being compared so they are of
            # the same length.
            a = normalize(a)
            b = normalize(b)
            values_len_max = len(max([a, b], key=len))
            for value in [a, b]:
                if len(value) < values_len_max:
                    value.extend([0] * (values_len_max - len(value)))

            # Compare all of the tokens until a difference is found.
            cmp_result = 0
            for cmp_values in zip(a, b):
                if all(isinstance(value, int) for value in cmp_values):
                    # If both tokens are integers, it's easy.
                    cmp_result = cmp(*cmp_values)
                else:
                    # Otherwise, if either happens to be an integer put it
                    # through the grinder as a string.
                    cmp_values = [str(value) for value in cmp_values]

                    # Pad mismatched strings with ASCII DEL (0x7f) for
                    # comparisons involving tilde
                    cmp_values_len_max = len(max(cmp_values, key=len))
                    cmp_values = [item.ljust(cmp_values_len_max, '\x7f')
                                  for item in cmp_values]

                    if len(set(cmp_values)) != 1:
                        if cmp_values[0] is sorted(cmp_values, key=key)[0]:
                            cmp_result = -1
                        else:
                            cmp_result = 1
                if cmp_result != 0:
                    break
            return cmp_result

        # Types changed while you wait!
        if isinstance(other, basestring):
            other = BaseVersion(other)
        elif not isinstance(other, BaseVersion):
            raise TypeError('Can only compare BaseVersion objects!')

        # First, compare epochs.  If there isn't one treat it as 0
        epochs = [0 if self.epoch is None else int(self.epoch),
                  0 if other.epoch is None else int(other.epoch)]
        epoch = cmp(*epochs)
        if epoch:
            return epoch

        # Next, compare the upstream_version part.
        upstream = cmp_part(self.upstream_version, other.upstream_version)
        if upstream:
            return upstream

        # Lastly, compare debian_version.  Even if this is not part of the
        # full version string, it will be compared as "0".
        debian = cmp_part(self.debian_version, other.debian_version)
        return debian


class DebianPackage:
    def __init__(self, path):
        self.path = path
        self.version = ""
        self.control = {}
        self.size = os.path.getsize(path)
        self.__load()

    def __load(self):
        has_flag = False
        has_control = False
        has_data = False
        # https://en.wikipedia.org/wiki/Deb_(file_format)
        fd = open(self.path, 'rb+')
        fd.seek(0)
        magic = fd.read(8)
        if magic != "!<arch>\n":
            raise IOError(_('Not a Debian Package'))
        while True:
            is_flag = False
            is_control = False
            is_data = False
            identifier_d = fd.read(16).rstrip()
            if len(identifier_d) == 0:
                break
            elif identifier_d == 'debian-binary':
                has_flag = True
                is_flag = True
            elif identifier_d[:7] == 'control':
                has_control = True
                is_control = True
            elif identifier_d[:4] == 'data':
                has_data = True
                is_data = True
            timestamp_d = fd.read(12).rstrip()
            ownerID_d = fd.read(6).rstrip()
            groupID_d = fd.read(6).rstrip()
            mode_d = fd.read(8).rstrip()
            size_d = fd.read(10).rstrip()
            endc = fd.read(2)
            if endc != '`\n':
                raise IOError(_('Malformed Debian Package'))
            size = int(size_d)
            if is_flag:
                if size != 4:
                    raise IOError(_('Malformed Debian Package'))
                else:
                    self.version = fd.read(4).rstrip()
            elif is_control:
                control_data = fd.read(size)
                temp = tempfile.NamedTemporaryFile(delete=False)
                temp.write(control_data)
                temp.close()
                control_tar = tarfile.open(temp.name, "r")
                control_names = control_tar.getnames()
                control_name = None
                if "./control" in control_names:
                    control_name = "./control"
                elif "control" in control_names:
                    control_name = "control"
                if control_name is None:
                    raise IOError('No Control Info')
                control_obj = control_tar.extractfile(control_name)
                control_content = control_obj.read()
                control_obj.close()
                control_tar.close()
                os.remove(temp.name)
                # http://man7.org/linux/man-pages/man5/deb-control.5.html
                required_cols = ['Package', 'Version']
                recommended_cols = ['Maintainer', 'Description', 'Architecture']
                cydia_cols = [
                    'Name', 'Depiction', 'Author', 'Sponsor', 'Icon'
                ]
                known_cols = [
                    'Package', 'Version',
                    'Maintainer', 'Description', 'Architecture',
                    'Name', 'Depiction', 'Author', 'Sponsor', 'Icon',
                    'Section', 'Priority', 'Installed-Size', 'Essential',
                    'Build-Essential', 'Origin', 'Bugs', 'Homepage',
                    'Tag', 'Multi-Arch', 'Source', 'Subarchitecture',
                    'Kernel-Version', 'Installer-Menu-Item', 'Depends',
                    'Pre-Depends', 'Recommends', 'Suggests', 'Breaks',
                    'Conflicts', 'Replaces', 'Provides', 'Built-Using',
                    'Built-For-Profiles'
                ]
                control_arr = control_content.split('\n')
                control_dict = {}
                all_cols = []
                last_col = ''
                for control_line in control_arr:
                    if len(control_line) == 0:
                        continue
                    if last_col == 'Description':
                        if control_line[:1] == ' ':
                            if control_line[1:] == '.':
                                control_dict[last_col] += '\n'
                            else:
                                control_dict[last_col] += control_line[1:] + '\n'
                    line_col = control_line.find(':')
                    if line_col > 0:
                        key = control_line[:line_col]
                        if key in known_cols:
                            value = control_line[line_col + 1:].strip()
                            all_cols.append(key)
                            control_dict.update({key: value})
                            last_col = key
                # Standard Check
                for required_col in required_cols:
                    if required_col not in all_cols:
                        raise IOError(_('Package missing required column: %s') % (required_col))
                for recommended_col in recommended_cols:
                    if recommended_col not in all_cols:
                        print(_('Package missing recommended column: %s') % (recommended_col))
                for cydia_col in cydia_cols:
                    if cydia_col not in all_cols:
                        print(_('Package missing Cydia column: %s') % (cydia_col))
                self.control = control_dict
            else:
                fd.seek(fd.tell() + size)
            if size % 2 == 1:
                fd.read(1)  # Even Padding
        if not (has_flag and has_control and has_data):
            raise IOError(_('Malformed Debian Package'))

    @staticmethod
    def value_for_field(field):
        if field is None:
            return None
        lt_index = field.find('<')
        if lt_index > 0:
            gt_index = field.find('>', lt_index)
            if gt_index > 0:
                return field[:lt_index].strip()
            else:
                return field
        else:
            return field

    @staticmethod
    def detail_for_field(field):
        if field is None:
            return None
        lt_index = field.find('<')
        if lt_index > 0:
            gt_index = field.find('>', lt_index)
            if gt_index > 0:
                return field[lt_index + 1:gt_index].strip()
            else:
                return field
        else:
            return field

    def control_content(self):
        content = ''
        for (control_key, control_value) in self.control.items():
            control_value = control_value.replace('\n', '\n ')
            control_value = control_value.replace('\n \n', '\n .\n')
            content += control_key + ': ' + control_value.replace('\n', '\n ') + '\n'
        return content
