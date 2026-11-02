#!/usr/bin/env python3
"""Read-only checks for a Cubism import PSD header or a self-contained model3 package."""
import argparse
import json
import struct
import sys
from pathlib import Path, PureWindowsPath


def readn(f, n):
    data = f.read(n)
    if len(data) != n:
        raise ValueError("文件提前结束")
    return data


def psd(path):
    with path.open("rb") as f:
        magic, ver, reserved, channels, height, width, depth, mode = struct.unpack(
            ">4sH6sHIIHH", readn(f, 26))
        if magic != b"8BPS" or ver != 1 or reserved != bytes(6):
            raise ValueError("不是标准 PSD 文件头（不接受改名的 PSB）")
        if not 0 < width <= 30000 or not 0 < height <= 30000 or not 1 <= channels <= 56:
            raise ValueError("PSD 画布或通道数无效")
        if mode != 3 or depth != 8:
            raise ValueError(f"载入副本需要 RGB、8 位/通道；实际模式={mode}，位深={depth}")
        size = path.stat().st_size
        def end_section():
            length, = struct.unpack(">I", readn(f, 4))
            end = f.tell() + length
            if end > size:
                raise ValueError("PSD 数据区长度超过文件边界")
            return end
        # Color mode data, image resources, layer/mask block. Count main layer
        # records only; groups are records too, not necessarily moving pieces.
        for _ in range(2):
            f.seek(end_section())
        layer_end = end_section()
        layers = None
        if f.tell() < layer_end:
            info_end = end_section()
            if info_end > layer_end:
                raise ValueError("主图层信息越过图层/蒙版数据区")
            if info_end > f.tell():
                if info_end-f.tell() < 2:
                    raise ValueError("主图层计数字段不完整")
                n, = struct.unpack(">h", readn(f, 2))
                layers=abs(n)
        f.seek(layer_end)
        compression, = struct.unpack(">H", readn(f, 2))
        if compression not in (0,1,2,3) or f.tell()>=size:
            raise ValueError("PSD 合成图像数据头无效或为空")
    return {"scope":"PSD 文件头与主要数据区；不解析每层像素、蒙版或 ICC 色彩配置",
            "canvas_px":[width,height], "mode":"RGB", "bits_per_channel":depth,
            "channels":channels,"main_layer_records_including_groups":layers,
            "next":"在 Photoshop 确认命名、实际拆层、sRGB、透明边缘与中性叠合；主图层计数不代表可动件数。"}


def json_object(path):
    data=json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data,dict):
        raise ValueError(f"JSON 顶层不是对象：{path.name}")
    return data


def runtime(index, package_root, expect_physics, extra_motions):
    base=index.parent
    root=(package_root or base).resolve()
    if not index.is_relative_to(root):
        raise ValueError("模型索引不在指定交付目录内")
    model=json_object(index)
    refs=model.get("FileReferences")
    if model.get("Version")!=3 or not isinstance(refs,dict):
        raise ValueError("需要 Version 3 的 model3.json 和 FileReferences")
    files=[]
    def resource(rel, field, kind):
        if not isinstance(rel,str) or not rel or PureWindowsPath(rel).anchor or "://" in rel:
            raise ValueError(f"{field} 必须是包内相对文件路径：{rel!r}")
        p=(base / rel.replace("\\","/")).resolve()
        if not p.is_relative_to(root):
            raise ValueError(f"{field} 指向包外：{rel}")
        if not p.is_file() or not p.stat().st_size:
            raise ValueError(f"{field} 引用缺失或空文件：{rel}")
        info={"field":field,"file":rel}
        if kind=="moc":
            with p.open("rb") as f:
                if readn(f,4)!=b"MOC3":
                    raise ValueError(f"{field} 没有 MOC3 签名：{rel}")
        elif kind=="texture":
            with p.open("rb") as f:
                head=readn(f,24)
            if head[:16]!=b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR":
                raise ValueError(f"{field} 不是含 IHDR 的 PNG：{rel}")
            w,h=struct.unpack(">II",head[16:24])
            if not w or not h:
                raise ValueError(f"{field} 纹理尺寸无效：{rel}")
            info["size_px"]=[w,h]
        elif kind=="json":
            json_object(p)
        files.append(info)
    resource(refs.get("Moc"),"Moc","moc")
    textures=refs.get("Textures")
    if not isinstance(textures,list) or not textures:
        raise ValueError("Textures 需要列出至少一张纹理")
    for i,rel in enumerate(textures):
        resource(rel,f"Textures[{i}]","texture")
    if expect_physics and not refs.get("Physics"):
        raise ValueError("约定的物理没有登记在 FileReferences.Physics")
    for key in ("Physics","DisplayInfo","Pose","UserData","MotionSync"):
        if key in refs:resource(refs[key],key,"json")
    def entries(entries_, field):
        if not isinstance(entries_,list) or any(not isinstance(x,dict) for x in entries_):
            raise ValueError(f"{field} 需要对象列表")
        return entries_
    for i,entry in enumerate(entries(refs.get("Expressions",[]),"Expressions")):
        resource(entry.get("File"),f"Expressions[{i}].File","json")
    groups=refs.get("Motions",{})
    if not isinstance(groups,dict):raise ValueError("Motions 应是按组组织的对象")
    for name,group in groups.items():
        for i,entry in enumerate(entries(group,f"Motions.{name}")):
            field=f"Motions.{name}[{i}]"
            resource(entry.get("File"),field+".File","json")
            if entry.get("Sound"):
                resource(entry["Sound"],field+".Sound","asset")
    for name in extra_motions:
        resource(name,"约定的额外动作","json")
    return {"scope":"包内路径、引用文件、MOC3 签名、PNG 文件头和 JSON 可读性；不加载模型或评价动画",
            "package_root":str(root),"checked_files":files,
            "next":"从此索引实际加载，核对关键部件与动作；真人面捕另行校准。"}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="mode",required=True)
    s=sub.add_parser("psd",help="检查载入 PSD 基本格式");s.add_argument("file",type=Path)
    s=sub.add_parser("runtime",help="检查 model3.json 的包内引用");s.add_argument("file",type=Path)
    s.add_argument("--root",type=Path,help="包的根目录；默认是索引所在目录")
    s.add_argument("--expect-physics",action="store_true",help="仅在约定有物理时要求 Physics")
    s.add_argument("--motion",action="append",default=[],help="额外需交付的动作相对路径，可重复")
    args=parser.parse_args(argv);path=args.file.resolve()
    try:
        details=psd(path) if args.mode=="psd" else runtime(path,args.root,args.expect_physics,args.motion)
        print(json.dumps({"ok":True,"file":str(path),**details},ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,RuntimeError) as exc:
        print(json.dumps({"ok":False,"file":str(path),"error":str(exc)},ensure_ascii=False))
        return 1

if __name__=="__main__":
    sys.exit(main())
