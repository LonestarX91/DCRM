# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-01-28 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WEIPDCRM', '0019_auto_20170128_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicetype',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled'),
        ),
        migrations.AlterField(
            model_name='osversion',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled'),
        ),
        migrations.AlterField(
            model_name='package',
            name='depiction',
            field=models.URLField(blank=True, default='', help_text='Pretty much the entire interface of Cydia is a webpage, which makes adding features or new functionality remotely very easy. One thing you might want is to be able to display custom links or screenshots with special formatting... just plain something special (even an advertisement) on your package page. This is done with a "depiction", which is a URL that is loaded into an iframe, replacing the Description: and Homepage: links that are normally presnt. For a good example see WinterBoard\'s package details page in Cydia. For many packagers this has simply become their More Information page, which is only used for backwards compatibility. It does not need to be the same, however. You also may consider not having a Homepage: field at all if you include Depiction:.', null=True, verbose_name='Depiction'),
        ),
        migrations.AlterField(
            model_name='package',
            name='description',
            field=models.TextField(blank=True, default='', help_text="This field is a little more complicated than the others, as it may use multiple lines. The first line (after the colon) should contain a short description to be displayed on the package lists underneath the name of the package. Optionally, one can choose to replace that description with an arbitrarily long one that will be displayed on the package details screen. Technically the format for this field is quite complicated, but most of that complexity is currently ignored by Cydia: instead Cydia allows you to place arbitrarily awesome HTML in this field. Each line of this extended description must begin with a space. I highly disrecommend using this for HTML, however: you should instead use Depiction: for the description in Cydia and use extended descriptions (which will then be ignored by Cydia) for compatibility with command-line clients. I would normally leave this mess undocumented, but this is so different from APT/dpkg that I feel the need to do a full explanation here. Arguably, at some future point, I should redo this field in Cydia to be parsed correctly, so another way of looking at this is that extended descriptions shouldn't be used with Cydia at all.", null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='package',
            name='enabled',
            field=models.BooleanField(default=False, verbose_name='Enabled'),
        ),
        migrations.AlterField(
            model_name='package',
            name='homepage',
            field=models.URLField(blank=True, default='', help_text='Often, there is more information that a packager wants to provide about a package than can be listed in the description of the package. Cydia supports a "More Info" field on the details screen that shunts users off to a website of the packager\'s choice.', null=True, verbose_name='Homepage'),
        ),
        migrations.AlterField(
            model_name='package',
            name='releases',
            field=models.ManyToManyField(blank=True, to='WEIPDCRM.Release', verbose_name='Releases'),
        ),
        migrations.AlterField(
            model_name='package',
            name='section',
            field=models.ForeignKey(blank=True, help_text='Under the "Install" tab in Cydia, packages are listed by "Section". If you would like to encode a space into your section name, use an underscore (Cydia will automatically convert these).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='WEIPDCRM.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='release',
            name='description',
            field=models.TextField(blank=True, help_text='On the package source screen a short description is listed of the repository. This description may eventually work similarly to that of a package (with a long/short variety and the aforementioned encoding), but for right now only the shorter description is displayed directly on the list.', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='active_release',
            field=models.ForeignKey(blank=True, help_text='Each repository should have an active release, otherwise it will not be recognized by any advanced package tools.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='WEIPDCRM.Release', verbose_name='Active Release'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='advanced_mode',
            field=models.BooleanField(default=True, help_text='Check it to generate awesome depiction page for each version.', verbose_name='Auto Depiction'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='downgrade_support',
            field=models.BooleanField(default=True, help_text='Enable this function will cause a long-term traffic consumption.', verbose_name='Downgrade Support'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='packages_compression',
            field=models.IntegerField(choices=[(0, 'plain'), (1, 'gzip'), (2, 'plain and gzip'), (3, 'bzip'), (4, 'plain and bzip'), (5, 'gzip and bzip'), (6, 'all')], default=6, help_text='Please change the compression method if error occurred when try to rebuild the list.', verbose_name='packages Compression'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='packages_validation',
            field=models.IntegerField(choices=[(0, 'No validation'), (1, 'MD5Sum'), (2, 'MD5Sum & SHA1'), (3, 'MD5Sum & SHA1 & SHA256'), (4, 'MD5Sum & SHA1 & SHA256 & SHA512')], default=1, help_text='It will not take effect until any version edited or added.', verbose_name='Packages Validation'),
        ),
        migrations.AlterField(
            model_name='version',
            name='control_field',
            field=models.TextField(blank=True, null=True, verbose_name='Control Field'),
        ),
        migrations.AlterField(
            model_name='version',
            name='device_compatibility',
            field=models.ManyToManyField(blank=True, to='WEIPDCRM.DeviceType', verbose_name='Device Compatibility'),
        ),
        migrations.AlterField(
            model_name='version',
            name='enabled',
            field=models.BooleanField(default=False, verbose_name='Enabled'),
        ),
        migrations.AlterField(
            model_name='version',
            name='os_compatibility',
            field=models.ManyToManyField(blank=True, to='WEIPDCRM.OSVersion', verbose_name='OS Compatibility'),
        ),
        migrations.AlterField(
            model_name='version',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WEIPDCRM.Package', verbose_name='Package'),
        ),
        migrations.AlterField(
            model_name='version',
            name='storage',
            field=models.FileField(upload_to='debs', verbose_name='Storage'),
        ),
        migrations.AlterField(
            model_name='version',
            name='update_logs',
            field=models.TextField(blank=True, null=True, verbose_name='Update Logs'),
        ),
    ]
