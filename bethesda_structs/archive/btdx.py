# Copyright (c) 2018 Stephen Bunn <stephen@bunn.io>
# GPLv3 License <https://choosealicense.com/licenses/gpl-3.0/>

import warnings
from enum import IntEnum
from typing import Tuple, Generator
from pathlib import PureWindowsPath

from construct import (
    Enum,
    Array,
    Bytes,
    Const,
    Int8ul,
    Struct,
    Switch,
    VarInt,
    Default,
    Int16ul,
    Int32ul,
    Int64ul,
    Container,
    FlagsEnum,
    Compressed,
    GreedyBytes,
    PaddedString,
    PascalString,
)

from .. import __version__
from ._common import ArchiveFile, BaseArchive
from ..contrib.dds import (
    DDS_HEADER,
    MAKEFOURCC,
    DDS_HEADER_DX10,
    DDS_PIXELFORMAT,
    DXGIFormats,
    D3D10ResourceDimension,
)


class BTDXArchive(BaseArchive):

    header_struct = Struct(
        "magic" / Bytes(4),
        "version" / Int32ul,
        "type" / PaddedString(4, "utf8"),
        "file_count" / Int32ul,
        "names_offset" / Int64ul,
    )
    file_struct = Struct(
        "hash" / Int32ul,
        "ext" / PaddedString(4, "utf8"),
        "directory_hash" / Int32ul,
        "_unknown_0" / Int32ul,
        "offset" / Int64ul,
        "packed_size" / Int32ul,
        "unpacked_size" / Int32ul,
        "_unknown_1" / Int32ul,
    )
    tex_header_struct = Struct(
        "hash" / Int32ul,
        "ext" / PaddedString(4, "utf8"),
        "directory_hash" / Int32ul,
        "_unknown_0" / Int8ul,
        "chunks_count" / Int8ul,
        "chunk_header_size" / Int16ul,
        "height" / Int16ul,
        "width" / Int16ul,
        "mips_count" / Int8ul,
        "format" / Int8ul,
        "_unknown_1" / Int16ul,
    )
    tex_chunk_struct = Struct(
        "offset" / Int64ul,
        "packed_size" / Int32ul,
        "unpacked_size" / Int32ul,
        "start_mip" / Int16ul,
        "end_mip" / Int16ul,
        "_unknown_0" / Int32ul,
    )
    tex_struct = Struct(
        "header" / tex_header_struct,
        "chunks" / Array(lambda this: this.header.chunks_count, tex_chunk_struct),
    )
    archive_struct = Struct(
        "header" / header_struct,
        "files"
        / Array(
            lambda this: this.header.file_count,
            Switch(
                lambda this: this.header.type, {"GNRL": file_struct, "DX10": tex_struct}
            ),
        ),
    )

    @classmethod
    def can_handle(cls, filepath: str) -> bool:
        """Determines if a given file can be handled by the current archive.

        Args:
            filepath (str): The filepath to check if can be handled

        Returns:
            bool: True if the file can be handled, otherwise False
        """
        header = cls.header_struct.parse_file(filepath)
        return header.magic == b"BTDX" and header.version >= 1

    def _build_dds_headers(self, file_container: Container) -> Tuple[bytes, bytes]:
        """Builds DDS and DX10 secion headers for a given `file_container`.

        Args:
            file_container (Container): File container to build headers for

        Returns:
            Tuple[bytes, bytes]: A tuple of `DDS_HEADER` and `DX10_HEADER` (maybe None)
        """

        header_data = {
            "dwFlags": {
                "DDSD_CAPS": True,
                "DDSD_HEIGHT": True,
                "DDSD_WIDTH": True,
                "DDSD_PIXELFORMAT": True,
                "DDSD_MIPMAPCOUNT": True,
                "DDSD_LINEARSIZE": True,
            },
            "dwHeight": file_container.header.height,
            "dwWidth": file_container.header.width,
            "dwMipMapCount": file_container.header.mips_count,
            "dwCaps": {
                "DDSCAPS_COMPLEX": True, "DDSCAPS_TEXTURE": True, "DDSCAPS_MIPMAP": True
            },
        }

        if file_container.header._unknown_1 == 2049:
            header_data.update(
                {
                    "dwCaps2": {
                        "DDSCAPS2_CUBEMAP": True,
                        "DDSCAPS2_CUBEMAP_POSITIVEX": True,
                        "DDSCAPS2_CUBEMAP_NEGATIVEX": True,
                        "DDSCAPS2_CUBEMAP_POSITIVEY": True,
                        "DDSCAPS2_CUBEMAP_NEGATIVEY": True,
                        "DDSCAPS2_CUBEMAP_POSITIVEZ": True,
                        "DDSCAPS2_CUBEMAP_NEGATIVEZ": True,
                    }
                }
            )

        # TODO: find a cleaner more ovbious way of implementing this logic
        dx10_header_data = {}
        pixel_data = {}
        if file_container.header.format == DXGIFormats.DXGI_FORMAT_BC1_UNORM:
            pixel_data.update(
                dict(
                    dwFlags=dict(DDPF_FOURCC=True),
                    dwFourCC=MAKEFOURCC("D", "X", "T", "1"),
                )
            )
            header_data.update(
                dict(
                    dwPitchOrLinearSize=(
                        (file_container.header.width * file_container.header.height)
                        // 2
                    )
                )
            )
        elif file_container.header.format == DXGIFormats.DXGI_FORMAT_BC2_UNORM:
            pixel_data.update(
                dict(
                    dwFlags=dict(DDPF_FOURCC=True),
                    dwFourCC=MAKEFOURCC("D", "X", "T", "3"),
                )
            )
            header_data.update(
                dict(
                    dwPitchOrLinearSize=(
                        file_container.header.width * file_container.header.height
                    )
                )
            )
        elif file_container.header.format == DXGIFormats.DXGI_FORMAT_BC3_UNORM:
            pixel_data.update(
                dict(
                    dwFlags=dict(DDPF_FOURCC=True),
                    dwFourCC=MAKEFOURCC("D", "X", "T", "5"),
                )
            )
            header_data.update(
                dict(
                    dwPitchOrLinearSize=(
                        file_container.header.width * file_container.header.height
                    )
                )
            )
        elif file_container.header.format == DXGIFormats.DXGI_FORMAT_BC5_UNORM:
            pixel_data.update(
                dict(
                    dwFlags=dict(DDPF_FOURCC=True),
                    dwFourCC=MAKEFOURCC("A", "T", "I", "2"),
                )
            )
            header_data.update(
                dict(
                    dwPitchOrLinearSize=(
                        file_container.header.width * file_container.header.height
                    )
                )
            )
        elif file_container.header.format in (
            DXGIFormats.DXGI_FORMAT_BC7_UNORM, DXGIFormats.DXGI_FORMAT_BC7_UNORM_SRGB
        ):
            # FIXME: There may be a header differnce between BC7_UNORM and
            # BC7_UNORM_SRGB, but I haven't noticed any
            # (someone with more experience will have to let me know)
            pixel_data.update(
                dict(
                    dwFlags=dict(DDPF_FOURCC=True),
                    dwFourCC=MAKEFOURCC("D", "X", "1", "0"),
                )
            )
            header_data.update(
                dict(
                    dwPitchOrLinearSize=(
                        file_container.header.width * file_container.header.height
                    )
                )
            )
            dx10_header_data.update(
                {
                    "dxgiFormat": file_container.header.format,
                    "resourceDimension": (
                        D3D10ResourceDimension.D3D10_RESOURCE_DIMENSION_TEXTURE2D.value
                    ),
                    "miscFlag": 0,
                    "arraySize": 1,
                    "miscFlags2": 0,
                }
            )
        elif file_container.header.format == DXGIFormats.DXGI_FORMAT_B8G8R8A8_UNORM:
            pixel_data.update(
                dict(
                    dwFlags=dict(DDPF_ALPHA=True, DDPF_RBG=True),
                    dwRGBBitCount=32,
                    dwABitMask=0xff000000,
                    dwRBitMask=0x00ff0000,
                    dwGBitMask=0x0000ff00,
                    dwBBitMask=0x000000ff,
                )
            )
            header_data.update(
                dict(
                    dwPitchOrLinearSize=(
                        (file_container.header.width * file_container.header.height) * 4
                    )
                )
            )
        elif file_container.header.format == DXGIFormats.DXGI_FORMAT_R8_UNORM:
            pixel_data.update(
                dict(
                    dwFlags=dict(DDPF_RGB=True), dwRGBBitCount=8, dwRBitMask=0x000000ff
                )
            )
            header_data.update(
                dict(
                    dwPitchOrLinearSize=(
                        file_container.header.width * file_container.header.height
                    )
                )
            )
        else:
            warnings.warn(
                (
                    f"unsupported DXGI format "
                    f"{DXGIFormats(file_container.header.format).name}, "
                    f"please create an issue on {__version__.__repo__} if you see this"
                ),
                UserWarning,
            )
            return

        header_data.update({"ddspf": pixel_data})
        dx10_header = None
        if len(dx10_header_data) > 0:
            dx10_header = DDS_HEADER_DX10.build(dx10_header_data)
        return (DDS_HEADER.build(header_data), dx10_header)

    def _iter_gnrl_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data for GNRL fiels and yields instances of
            `ArchiveFile`.

        Raises:
            ValueError: If a filename cannot be determined for a specific file record

        Yields:
            ArchiveFile: An file contained within the archive
        """
        filename_offset = 0
        for (file_idx, file_container) in enumerate(self.container.files):
            filepath_content = self.content[
                (self.container.header.names_offset + filename_offset):
            ]
            filepath = PascalString(VarInt, "utf8").parse(filepath_content)
            # filename offset increased by length of parsed string accounting for
            # prefix and suffix bytes
            filename_offset += len(filepath) + 2

            file_data = self.content[
                file_container.offset:(
                    file_container.offset + file_container.unpacked_size
                )
            ]
            if file_container.packed_size > 0:
                file_data = Compressed(GreedyBytes, "zlib").parse(file_data)

            yield ArchiveFile(
                filepath=PureWindowsPath(filepath[1:]),
                data=file_data,
            )

    def _iter_dx10_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data for DX10 archives and yields instances of
            `ArchiveFile`.

        Raises:
            ValueError: If a filename cannot be determined for a specific file record

        Yields:
            ArchiveFile: An file contained within the archive
        """
        filename_offset = 0
        for (file_idx, file_container) in enumerate(self.container.files):

            filepath_content = self.content[
                (self.container.header.names_offset + filename_offset):
            ]
            filepath = PascalString(Int16ul, "utf8").parse(filepath_content)
            filename_offset += len(filepath) + 2

            (dds_header, dx10_header) = self._build_dds_headers(file_container)
            if dds_header:
                dds_content = b"DDS "
                dds_content += dds_header

                if dx10_header:
                    dds_content += dx10_header

                for tex_chunk in file_container.chunks:
                    if tex_chunk.packed_size > 0:
                        dds_content += Compressed(GreedyBytes, "zlib").parse(
                            self.content[
                                tex_chunk.offset:(
                                    tex_chunk.offset + tex_chunk.packed_size
                                )
                            ]
                        )
                    else:
                        dds_content += self.content[
                            tex_chunk.offset:(
                                tex_chunk.offset + tex_chunk.unpacked_size
                            )
                        ]

                yield ArchiveFile(filepath=PureWindowsPath(filepath), data=dds_content)

    def iter_files(self) -> Generator[ArchiveFile, None, None]:
        """Iterates over the parsed data and yields instances of `ArchiveFile`

        Raises:
            ValueError: If a filename cannot be determined for a specific file record

        Yields:
            ArchiveFile: An file contained within the archive
        """
        iter_method = {"GNRL": self._iter_gnrl_files, "DX10": self._iter_dx10_files}[
            self.container.header.type
        ]
        for archive_file in iter_method():
            yield archive_file
