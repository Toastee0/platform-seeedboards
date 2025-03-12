# SPDX-License-Identifier: Apache-2.0
"""
Arduino
Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.
https://github.com/SiliconLabs/arduino
"""

from os.path import isdir, join
import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduino-silabs")
CORE_DIR = join(FRAMEWORK_DIR, "cores", board.get("build.core"))
VARIANTS_DIR = join(FRAMEWORK_DIR, "variants", board.get("build.variant"))
build_tool_dir = platform.get_package_dir("toolchain-gccarmnoneeabi")
print("FRAMEWORK_DIR=:",FRAMEWORK_DIR)
print("CORE_DIR=:",CORE_DIR)
print("VARIANTS_DIR=:",VARIANTS_DIR)
assert isdir(FRAMEWORK_DIR)
assert isdir(CORE_DIR)



var = join(VARIANTS_DIR,"matter","gecko_sdk_4.4.0","platform","common","toolchain","inc","sl_gcc_preinclude.h")
_var = join(VARIANTS_DIR,"matter","config","psa_crypto_config.h")
_var_ = join(VARIANTS_DIR,"matter","config","sl_mbedtls_config.h")
print("_var =:",_var)
print("_var_ =:",_var_)
env.Append(
    CFLAGS=["-std=c99"],

    CCFLAGS=[
        "-mthumb",
        "-mcpu=cortex-m33",
        "-mfpu=fpv5-sp-d16",
        "-mfloat-abi=hard",
        "-Wno-cast-function-type",
        "-Wno-psabi",
        "-Wno-sign-compare",
        "-c",
        "-Wno-missing-field-initializers",
        "-fdata-sections",
        "-fomit-frame-pointer",
        "--specs=nano.specs",
        "-Wall",
        "-imacros",
        f"{var}",
        "-mcmse",
        "-Wextra",
        "-w",
        "-Wno-unused-parameter",
        "-Wno-maybe-uninitialized",
        "-ffunction-sections",
        "-Wno-deprecated-declarations",
        "-g"
    ],
    
    CXXFLAGS=[
        # "-std=c++11",
        "-std=gnu++17",
        "-fno-common",
        "-fno-unwind-tables",
        "-fno-asynchronous-unwind-tables",
        "-fno-strict-aliasing",
        "-fno-exceptions"
    ],

    LINKFLAGS=[
        "-mcpu=cortex-m33",
        "-mthumb",
        "-mfpu=fpv5-sp-d16",
        "-mfloat-abi=hard",
        "--specs=nano.specs",
        "-Wl,--gc-sections"
    ],

    CPPDEFINES=[
        ("F_CPU", "39000000"),
        "ARDUINO=10607",
        "ARDUINO_XIAO_MG24",
        "ARDUINO_ARCH_SILABS",
        "ARDUINO_SILABS=2.3.0",
        "EFR32MG24B220F1536IM48",
        'NUM_LEDS=1',
        'NUM_HW_SERIAL=2',
        'NUM_HW_SPI=2',
        'NUM_HW_I2C=2',
        'NUM_DAC_HW=2',
        'ARDUINO_MAIN_TASK_STACK_SIZE=2048'
        "HARDWARE_BOARD_DEFAULT_RF_BAND_2400",
        "HARDWARE_BOARD_SUPPORTS_1_RF_BAND",
        "HARDWARE_BOARD_SUPPORTS_RF_BAND_2400",
        "HFXO_FREQ=39000000",
        "SL_BOARD_NAME=\"BRD4187C\"",
        "SL_BOARD_REV=\"A01\"",
        "SL_COMPONENT_CATALOG_PRESENT=1",
        "configNUM_SDK_THREAD_LOCAL_STORAGE_POINTERS=2"
        # f"MBEDTLS_CONFIG_FILE=<{_var_}>",
        # f"MBEDTLS_PSA_CRYPTO_CONFIG_FILE=<{_var}>"
    ],

    LIBS=["m", "stdc++", "gcc", "c", "m", "nosys", "supc++"]
)

# TODO
# for sub-variants matter. ble, noradio
# get cflags, cxxflags, ldflags etc. from
# https://github.com/SiliconLabs/arduino/blob/main/platform.txt
# https://github.com/SiliconLabs/arduino/blob/main/boards.txt


#
# Target: Build Core Library
#
env.Append(
    # Due to long path names "-iprefix" hook is required to avoid toolchain crashes
    ASFLAGS=[
        "-iprefix" + os.path.join(VARIANTS_DIR, "matter"),
        "@%s" % os.path.join(VARIANTS_DIR, "matter", "includes.txt")

    ],

    CCFLAGS=[
        "-iprefix" + os.path.join(VARIANTS_DIR, "matter"),
        "@%s" % os.path.join(VARIANTS_DIR, "matter", "includes.txt")

    ],

    CPPPATH=[
        os.path.join(CORE_DIR),
        os.path.join(FRAMEWORK_DIR, "cores", board.get(
            "build.core"), "api"),
        os.path.join(FRAMEWORK_DIR, "cores", board.get(
            "build.core"), "api", "deprecated"),
        os.path.join(FRAMEWORK_DIR, "cores", board.get(
            "build.core"), "api", "deprecated-avr-comp","avr")
    ],

)


libs = []

if "build.variant" in board:

    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants", board.get("build.variant"))
        ]
    )

    libs.append(
        env.BuildLibrary(
            join("$BUILD_DIR", "FrameworkArduinoVariant"),
            join(FRAMEWORK_DIR, "variants", board.get("build.variant"))
        ))

libs.append(
    env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduino"),
        join(CORE_DIR)))

env.Prepend(LIBS=libs)