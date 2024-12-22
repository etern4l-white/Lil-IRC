# Lil-IRC
Screw matrix tools, all my homies use IRC.

- [1](https://datatracker.ietf.org/doc/html/rfc2810)

## Messages format for now

```json
{
    "user":"<username>",
    "message":"<actual_message>"
}
```

# Notes

## Phase 1

Implementing a terminal-based IRC + concurrent connections + auth

- [x] For client, make sending and receiving on separate threads. Each in a different color.
- [x] For clients, make the whole thing with ncurses.
- [ ] Gotta work well on the interface, fix the following:
    - [x] Current messages have to be in a queue, both client and server messages.
    - [ ] handle mutli-line messages and mutli-line buffers.
    - [x] emphasize my messages (green + bold).
- [ ] handle files:
    - [ ] upload file from client side, via file path.
    - [ ] download file on server, idk how I'll implement this on other clients' sides.
- [x] Make the code in functions...
- [x] standardize format between client and server.
- [ ] handle concurrent connections (mutltiple clients)
- [ ] broadcast messages
- [ ] identify users (basic register/login logic)
- [ ] fix connection bugs, log errors/bugs for servers and clients.
- [ ] make the code OOP, you actually need that lol...