# SPDX-License-Identifier: MIT
# Copyright (c) 2026 ProStaking contributors
"""Optional offline config editor, extracted unchanged from the reviewed runbook.
Requires STATE containing socket.toml and IFACE naming that same standalone port.
Writes only STATE/xdp.toml; does not install it, restart services or modify networks.
See docs/runbook.md for preconditions and mandatory diff review.
"""
import os, pathlib, re, tomllib
state = pathlib.Path(os.environ['STATE'])
text = (state/'socket.toml').read_text()
original = tomllib.loads(text)
assert original['net']['provider'] == 'socket', 'Require explicit socket baseline'
assert original['net']['interface'] == os.environ['IFACE'], 'Require same standalone port'
updates = {'net': {'provider': 'xdp'}, 'net.xdp': {
    'xdp_mode': 'drv', 'native_bond': 'false', 'xdp_zero_copy': 'true',
    'poll_mode': 'softirq', 'rss_queue_mode': 'simple'}}
for section, values in updates.items():
    pattern = r'(?m)^[ \t]*\[' + re.escape(section) + r'\][ \t]*(?:#.*)?$'
    matches = list(re.finditer(pattern, text))
    assert len(matches) <= 1
    if not matches:
        text += '\n[' + section + ']\n'
        matches = list(re.finditer(pattern, text))
    start = matches[0].end()
    following = re.search(r'(?m)^[ \t]*\[', text[start:])
    end = start + following.start() if following else len(text)
    body = text[start:end]
    for key, value in values.items():
        line = f'{key} = "{value}"'
        key_pattern = r'(?m)^[ \t]*' + re.escape(key) + r'[ \t]*=.*$'
        if re.search(key_pattern, body):
            body = re.sub(key_pattern, line, body)
        else:
            body += '\n' + line + '\n'
    text = text[:start] + body + text[end:]
candidate = tomllib.loads(text)
expected = tomllib.loads((state/'socket.toml').read_text())
expected['net']['provider'] = 'xdp'
expected['net'].setdefault('xdp', {}).update(updates['net.xdp'])
assert candidate == expected, 'Unexpected config change'
path = state/'xdp.toml'
path.write_text(text)
path.chmod(0o600)
