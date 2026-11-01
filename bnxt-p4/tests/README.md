# Tests and their scope

Driver: the reconstructed source includes the full tests directory. In `p4-experimental` run `sh "$PACKAGE/tests/run-driver-tests.sh"` with Python3, C compiler and sanitizer runtime available. Keep sibling research-driver. All27 suites passed in the retained Debian12/GCC12.2 environment; modeled firmware/DMA/kernel primitives do not prove silicon teardown. This packaging pass replays source patches and verifies bytes; it does not rerun builds/tests. Earlier mutation campaign62/63 killed had one equivalent survivor.

Firedancer pure primitives:

```sh
gcc-12 -std=c17 -Wall -Wextra -Werror -O2 src/waltz/xdp/test_xsk_prebind.c -o /tmp/test_xsk_prebind
/tmp/test_xsk_prebind
gcc-12 -std=c17 -Wall -Wextra -Werror -O2 -Isrc "$PACKAGE/tests/test_init.c" -o /tmp/test_init
/tmp/test_init
gcc-12 -std=c17 -Wall -Wextra -Werror -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -Isrc "$PACKAGE/tests/test_init.c" -o /tmp/test_init_san
ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 /tmp/test_init_san
```

Nine mocked-syscall cases test actual fd_xsk_init behavior plus pure layout/publication checks. Full default/opt-in executables linked. Ordinary repository test_xsk runtime was unavailable in the container because NUMA sysfs was absent. Private activation/recovery tooling had53 guard tests then65 restoration tests and independent review; that site-specific tooling is not included or claimed portable here.
