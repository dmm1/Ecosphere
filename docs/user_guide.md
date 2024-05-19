# Using Redis on Windows

To install Redis on Windows, you can use the MicrosoftArchive Redis version. Follow these steps:

1. Download the latest Redis .msi file from the [releases page](https://github.com/microsoftarchive/redis/releases).

2. Run the .msi file and follow the instructions. By default, it will be installed in `C:\Program Files\Redis`.

3. After installation, the Redis service will start automatically. You can check if Redis is working by opening Command Prompt and typing:

```bash
redis-cli ping
```
If Redis is running, it will return PONG.

To start Redis manually, you can use:

```bash
redis-server
```