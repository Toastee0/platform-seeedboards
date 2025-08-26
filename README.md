# Seeed Xiao NRF54L15 Series: Experimental modified board definitions
#Fixed set of board definitions that allow platform.io to work, follow the seeed wiki instructions, but use this repository instead of the official seed one.

main changes:
Added the line to NRF54l15.json, this corrects platform IO failing to find the board definitions.
```
"Varient": " SEEED_XIAO_NRF54L15",
```
Copied in nordic include dtsi files, and included them directly, instead of depending on them to being present externally. (added these lines to the SOC def @ xiao_nrf54l15_nrf54l15_cpuapp.dts)
```
#include "nrf54l_05_10_15_cpuapp.dtsi"
#include "nrf54l_cpuapp.dtsi"
#include "nrf54l15.dtsi"
```

and the addition of these lines to enable various SOC perihperials. platform-seeedboards\zephyr\boards\arm\xiao_nrf54l15\xiao_nrf54l15_nrf54l15_cpuapp.dts
```
&radio {
	status = "okay";
};

&ieee802154 {
	status = "okay";
};

&temp {
	status = "okay";
};

&clock {
	status = "okay";
};

&nfct {
    status = "okay";
};
```


# Seeed Xiao Series: development platform for [PlatformIO](http://platformio.org)

[![Build Status](https://travis-ci.org/platformio/platform-atmelsam.svg?branch=develop)](https://travis-ci.org/platformio/platform-atmelsam)
[![Build status](https://ci.appveyor.com/api/projects/status/dj1c3b2d6fyxkoxq/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-atmelsam/branch/develop)

The [Seeed Studio XIAO Series](https://wiki.seeedstudio.com/SeeedStudio_XIAO_Series_Introduction/) is a collection of thumb-sized, powerful microcontroller units (MCUs) tailor-made for space-conscious projects requiring high performance and wireless connectivity.

* [Home](http://platformio.org/platforms/seeedxiao) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/seeedxiao.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Development version

```ini
[env:development]
platform = https://github.com/Toastee0/platform-seeedboards.git
board = ...
framework = arduino
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/seeedxiao.html).
