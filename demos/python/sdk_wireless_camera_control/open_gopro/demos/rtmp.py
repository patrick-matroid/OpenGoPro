from open_gopro.demos.gui.components.models import CompoundGoPro
from open_gopro.util import add_cli_args_and_parse
import asyncio
import argparse
from open_gopro import proto
from open_gopro.logger import setup_logging
from rich.console import Console
console = Console()
async def main(args: argparse.Namespace) -> None:
    setup_logging(__name__, args.log)
    async with CompoundGoPro(args.identifier) as gopro:
        assert(await gopro.compound_command.livestream(url=args.url, 
                                                      ssid=args.ssid, 
                                                      password=args.password,
                                                      window_size=args.resolution,
                                                      lens_type=args.fov,
                                                      min_bit=args.min_bit,
                                                      max_bit=args.max_bit,
                                                      start_bit=args.start_bit)).ok

 

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the GoPro via BLE only, configure then start a Livestream, then display it with CV2."
    )
    parser.add_argument("--ssid", type=str, help="WiFi SSID to connect to.")
    parser.add_argument("--password", type=str, help="Password of WiFi SSID.")
    parser.add_argument("--url", type=str,default='rtmp://192.168.86.132/live/f9cea3f079', help="RTMP server URL to stream to.")
    parser.add_argument("--min_bit", type=int, help="Minimum bitrate.", default=4500)
    parser.add_argument("--max_bit", type=int, help="Maximum bitrate.", default=8000)
    parser.add_argument("--start_bit", type=int, help="Starting bitrate.", default=1000)
    parser.add_argument(
        "--resolution",
        help="Resolution.",
        choices=list(proto.EnumWindowSize.DESCRIPTOR.values_by_number.keys()),
        default=proto.EnumWindowSize.WINDOW_SIZE_1080,
    )
    parser.add_argument(
        "--fov",
        help="Field of View.",
        choices=[],
        default=proto.EnumLens.LENS_LINEAR,
    )
    return add_cli_args_and_parse(parser, wifi=False)


def entrypoint() -> None:
    asyncio.run(main(parse_arguments()))


if __name__ == "__main__":
    entrypoint()
