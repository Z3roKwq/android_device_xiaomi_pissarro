#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools


from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/pissarro',
    'hardware/mediatek',
    'hardware/xiaomi',
    'vendor/xiaomi/pissarro',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('libsink',): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/lib/libmtkcam_stdutils.so',
        'vendor/lib64/libmtkcam_stdutils.so',
        'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so',
        'vendor/lib/hw/vendor.mediatek.hardware.pq@2.13-impl.so',
        'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.13-impl.so'
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    (
        'vendor/bin/hw/android.hardware.gnss-service.mediatek',
        'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'
    ): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    (
        'system_ext/lib64/libsource.so'
    ): blob_fixup()
        .add_needed('libui_shim.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib/libaalservice.so',
        'vendor/lib64/libaalservice.so',
        'vendor/lib64/libcam.utils.sensorprovider.so'
    ): blob_fixup()
        .add_needed('libshim_sensors.so'),
    (
        'system_ext/lib64/libsink.so'
    ): blob_fixup()
        .add_needed('libshim_sink.so'),
    (
        'vendor/etc/init/init.batterysecret.rc'
    ): blob_fixup()
        .regex_replace(r'.*seclabel.*\n', ''),
    (
        'vendor/etc/init/android.hardware.neuralnetworks@1.3-service-mtk-neuron.rc'
    ): blob_fixup()
        .regex_replace('start', 'enable'),
    (
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b',
        'vendor/bin/hw/vendor.dolby.hardware.dms@2.0-service'
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    (
        'vendor/etc/init/android.hardware.bluetooth@1.1-service-mediatek.rc'
    ): blob_fixup()
        .regex_replace(r'on property.*\n.*\n', ''),
}

module = ExtractUtilsModule(
    'pissarro',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()