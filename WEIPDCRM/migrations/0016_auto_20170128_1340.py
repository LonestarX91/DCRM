# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-28 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WEIPDCRM', '0015_package_architecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='architectures',
            field=models.CharField(blank=True, default='iphoneos-arm', help_text='To verify a repository is for the specific device you are working with APT looks in the release file for this list. You must specify all of the architectures that appear in your Packages file here. Again, we use darwin-arm for 1.1.x and iphoneos-arm for 2.x.', max_length=255, verbose_name='Architectures'),
        ),
        migrations.AddField(
            model_name='release',
            name='components',
            field=models.CharField(blank=True, default='main', help_text='Just set this to "main". This field might not be required, but who really knows? I, for certain, do not.', max_length=255, verbose_name='Components'),
        ),
        migrations.AddField(
            model_name='release',
            name='suite',
            field=models.CharField(blank=True, default='stable', help_text='Just set this to "stable". This field might not be required, but who really knows? I, for certain, do not.', max_length=255, verbose_name='Suite'),
        ),
        migrations.AlterField(
            model_name='package',
            name='architecture',
            field=models.CharField(default='', help_text='This describes what system a package is designed for, as .deb files are used on everything from the iPhone to your desktop computer. The correct value for iPhoneOS 1.0.x/1.1.x is "darwin-arm". If you are deploying to iPhoneOS 1.2/2.x you should use "iphoneos-arm".', max_length=255, verbose_name='Architecture'),
        ),
        migrations.AlterField(
            model_name='package',
            name='author_name',
            field=models.CharField(blank=True, help_text='In contrast, the person who wrote the original software is called the "author". This name will be shown underneath the name of the package on the details screen. The field is in the same format as "Maintainer".', max_length=255, null=True, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='package',
            name='depiction',
            field=models.URLField(blank=True, default='', help_text='Pretty much the entire interface of Cydia is a webpage, which makes adding features or new functionality remotely very easy. One thing you might want is to be able to display custom links or screenshots with special formatting... just plain something special (even an advertisement) on your package page. This is done with a "depiction", which is a URL that is loaded into an iframe, replacing the Description: and Homepage: links that are normally presnt. For a good example see WinterBoard\'s package details page in Cydia. For many packagers this has simply become their More Information page, which is only used for backwards compatibility. It does not need to be the same, however. You also may consider not having a Homepage: field at all if you include Depiction:.', null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='description',
            field=models.TextField(blank=True, default='', help_text="This field is a little more complicated than the others, as it may use multiple lines. The first line (after the colon) should contain a short description to be displayed on the package lists underneath the name of the package. Optionally, one can choose to replace that description with an arbitrarily long one that will be displayed on the package details screen. Technically the format for this field is quite complicated, but most of that complexity is currently ignored by Cydia: instead Cydia allows you to place arbitrarily awesome HTML in this field. Each line of this extended description must begin with a space. I highly disrecommend using this for HTML, however: you should instead use Depiction: for the description in Cydia and use extended descriptions (which will then be ignored by Cydia) for compatibility with command-line clients. I would normally leave this mess undocumented, but this is so different from APT/dpkg that I feel the need to do a full explanation here. Arguably, at some future point, I should redo this field in Cydia to be parsed correctly, so another way of looking at this is that extended descriptions shouldn't be used with Cydia at all.", null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='homepage',
            field=models.URLField(blank=True, default='', help_text='Often, there is more information that a packager wants to provide about a package than can be listed in the description of the package. Cydia supports a "More Info" field on the details screen that shunts users off to a website of the packager\'s choice.', null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.CharField(help_text='When the package is shown in Cydia\'s lists, it is convenient to have a prettier name. This field allows you to override this display with an arbitrary string. This field may change often, whereas the "Package" field is fixed for the lifetime of the package.', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='package',
            name='package',
            field=models.CharField(help_text='This is the "identifier" of the package. This should be, entirely in lower case, a reversed hostname (much like a "bundleIdentifier" in Apple\'s Info.plist files). If you are also choosing to host an AppTapp Installer repository to support legacy clients, you are strongly encouraged to make this name match the AppTapp bundle identifier (except all in lower case).', max_length=255, unique=True, verbose_name='Package'),
        ),
        migrations.AlterField(
            model_name='package',
            name='section',
            field=models.ForeignKey(help_text='Under the "Install" tab in Cydia, packages are listed by "Section". If you would like to encode a space into your section name, use an underscore (Cydia will automatically convert these).', on_delete=django.db.models.deletion.CASCADE, to='WEIPDCRM.Section'),
        ),
        migrations.AlterField(
            model_name='package',
            name='sponsor_name',
            field=models.CharField(blank=True, help_text='Finally, there might be someone who is simply providing the influence or the cash to make the package happen. This person should be listed here in the form of "Maintainer" except using a resource URI instead of an e-mail address.', max_length=255, null=True, verbose_name='Sponsor'),
        ),
        migrations.AlterField(
            model_name='release',
            name='codename',
            field=models.CharField(default='', help_text='In an "automatic" repository you might store multiple distributions of software for different target systems. For example: apt.saurik.com\'s main repository houses content both for desktop Debian Etch systems as well as the iPhone. This codename then describes what distribution we are currently looking for. In a "trivial" repository (as described in this document) you may put anything you want here, and the field may even be optional.', max_length=255, verbose_name='Codename'),
        ),
        migrations.AlterField(
            model_name='release',
            name='description',
            field=models.TextField(blank=True, help_text='On the package source screen a short description is listed of the repository. This description may eventually work similarly to that of a package (with a long/short variety and the aforementioned encoding), but for right now only the shorter description is displayed directly on the list.'),
        ),
        migrations.AlterField(
            model_name='release',
            name='keywords',
            field=models.CharField(blank=True, default='', help_text='Separated by commas.', max_length=255, verbose_name='Keywords'),
        ),
        migrations.AlterField(
            model_name='release',
            name='label',
            field=models.CharField(default='', help_text="On the package list screens, Cydia shows what repository and section packages came from. This location doesn't have much room, though, so this field should contain a shorter/simpler version of the name of the repository that can be used as a tag.", max_length=255, verbose_name='Label'),
        ),
        migrations.AlterField(
            model_name='release',
            name='origin',
            field=models.CharField(default='', help_text='This is used by Cydia as the name of the repository as shown in the source editor (and elsewhere). This should be a longer, but not insanely long, description of the repository.', max_length=255, verbose_name='Origin'),
        ),
        migrations.AlterField(
            model_name='release',
            name='version',
            field=models.CharField(default='0.0.1-1', help_text='This is an arbitrary version number that nothing actually parses. I am going to look into seeing how required it is.', max_length=255, verbose_name='Version'),
        ),
        migrations.AlterField(
            model_name='version',
            name='version',
            field=models.CharField(default='0.0.1-1', help_text="A package's version indicates two separate values: the version of the software in the package, and the version of the package itself. These version numbers are separated by a hyphen.", max_length=255, verbose_name='Version'),
        ),
    ]
