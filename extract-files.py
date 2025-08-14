#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)

namespace_imports = [
    'device/xiaomi/pissarro',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
    'vendor/xiaomi/pissarro',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups
}

blob_fixups: blob_fixups_user_type = {
    (
        'system/priv-app/ImsService/ImsService.apk'
    ): blob_fixup()
        .apktool_patch('blob-patches/ImsService.patch'),
    (
        'system/framework/mediatek-telephony-base.jar'
    ): blob_fixup()
        .apktool_patch('blob-patches/MediatekTelephonyBase.patch'),
    (
        'system/lib64/libsink-mtk.so'
    ): blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    (
        'system/lib64/libimsma.so'
    ): blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    (
        'system/lib64/libsource.so'
    ): blob_fixup()
        .add_needed('libui_shim.so'),
    (
        'vendor/bin/hw/android.hardware.gnss-service.mediatek',
        'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'
    ): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    (
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b'
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    (
        'vendor/etc/init/android.hardware.media.c2@1.2-mediatek.rc'
    ): blob_fixup()
        .regex_replace('@1.2-mediatek\n', '@1.2-mediatek-64b\n'),
    (
        'vendor/etc/init/android.hardware.bluetooth@1.1-service-mediatek.rc'
    ): blob_fixup()
        .regex_replace('on property[^\n]*\n[^\n]*\n', ''),
    (
        'vendor/etc/init/android.hardware.neuralnetworks@1.3-service-mtk-neuron.rc'
    ): blob_fixup()
        .regex_replace('start', 'enable'),
    (
        'vendor/etc/init/init.batterysecret.rc'
    ): blob_fixup()
        .regex_replace('.*seclabel.*\n', ''),
    (
        'vendor/lib/hw/audio.primary.mt6877.so'
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libalsautils.so', 'libalsautils-v31.so'),
    (
        'vendor/lib64/hw/hwcomposer.mt6877.so'
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron',
        'vendor/lib/libnvram.so',
        'vendor/lib64/libnvram.so',
        'vendor/lib64/libsysenv.so'
    ): blob_fixup()
        .add_needed('libbase_shim.so'),
    (
        'vendor/lib/hw/vendor.mediatek.hardware.pq@2.13-impl.so',
        'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.13-impl.so',
        'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so',
        'vendor/lib64/libmtkcam_stdutils.so'
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib/libaalservice.so',
        'vendor/lib64/libaalservice.so',
        'vendor/lib64/libcam.utils.sensorprovider.so'
    ): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    (
        'vendor/lib/libteei_daemon_vfs.so',
        'vendor/lib64/lib3a.ae.stat.so',
        'vendor/lib64/lib3a.flash.so',
        'vendor/lib64/lib3a.sensors.color.so',
        'vendor/lib64/lib3a.sensors.flicker.so',
        'vendor/lib64/libaaa_ltm.so',
        'vendor/lib64/libteei_daemon_vfs.so',
        'vendor/lib64/libSQLiteModule_VER_ALL.so'
    ): blob_fixup()
        .add_needed('liblog.so'),
    (
        'vendor/lib64/libmnl.so'
    ): blob_fixup()
        .add_needed('libcutils.so'),
    (
        'vendor/lib64/libdlbdsservice.so'
    ): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
}

module = ExtractUtilsModule(
    'pissarro',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()