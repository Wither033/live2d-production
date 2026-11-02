"""Local smoke tests only: no Photoshop, Cubism, VTS, network or user model."""
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from zlib import crc32, compress

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from preflight import psd, runtime


def u32(b):return struct.pack(">I",len(b))+b


def small_psd():
    def layer(name):
        label=bytes([len(name)])+name
        extra=u32(b"")+u32(b"")+label.ljust((len(label)+3)//4*4,b"\0")
        channels=b''.join(struct.pack(">hI",i,3) for i in (0,1,2,-1))
        return struct.pack(">iiiiH",0,0,1,1,4)+channels+b"8BIMnorm\xff\0\0\0"+u32(extra)
    records=layer(b"face")+layer(b"eye")
    planes=b''.join(b'\0\0'+bytes([i]) for i in (127,63,255,255,0,0,0,255))
    info=struct.pack(">h",2)+records+planes
    return (struct.pack(">4sH6sHIIHH",b"8BPS",1,bytes(6),3,1,1,8,3)
            +u32(b"")+u32(b"")+u32(u32(info)+u32(b""))+b"\0\0\x7f\x3f\xff")


def png():
    def chunk(name,data):
        return struct.pack(">I",len(data))+name+data+struct.pack(">I",crc32(name+data)&0xffffffff)
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack(">IIBBBBB",1,1,8,6,0,0,0))
            +chunk(b'IDAT',compress(bytes([0,128,128,128,255])))+chunk(b'IEND',b''))


class Preflight(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.pkg=Path(self.temp.name)/"演示";self.pkg.mkdir()
        self.idx=self.pkg/"角色.model3.json"
        (self.pkg/"角色.moc3").write_bytes(b"MOC3header fixture, not a renderable model")
        (self.pkg/"texture.png").write_bytes(png())
        self.refs={"Moc":"角色.moc3","Textures":["texture.png"]}
        self.save()
    def tearDown(self):self.temp.cleanup()
    def save(self):self.idx.write_text(json.dumps({"Version":3,"FileReferences":self.refs}),encoding="utf-8")
    def check(self,phys=False,motions=()):return runtime(self.idx.resolve(),None,phys,motions)

    def test_split_psd_metadata(self):
        p=self.pkg/"载入.psd";p.write_bytes(small_psd())
        info=psd(p);self.assertEqual(info["main_layer_records_including_groups"],2)
        self.assertEqual(info["canvas_px"],[1,1])

    def test_wrong_psd_or_truncated(self):
        p=self.pkg/"载入.psd"; raw=bytearray(small_psd());raw[22:24]=b"\0\x10"
        p.write_bytes(raw)
        with self.assertRaisesRegex(ValueError,"8 位"):psd(p)
        p.write_bytes(small_psd()[:28])
        with self.assertRaises(ValueError):psd(p)

    def test_physics_is_optional_until_promised(self):
        self.assertEqual(len(self.check()["checked_files"]),2)
        with self.assertRaisesRegex(ValueError,"物理没有登记"):self.check(phys=True)
        self.refs["Physics"]="p.physics3.json";self.save()
        with self.assertRaisesRegex(ValueError,"p.physics3.json"):self.check(phys=True)

    def test_missing_nested_asset_and_external_path(self):
        self.refs["Motions"]={"Idle":[{"File":"motion/idle.motion3.json"}]};self.save()
        with self.assertRaisesRegex(ValueError,"idle.motion3.json"):self.check()
        self.refs.pop("Motions");self.refs["Textures"]=["../out.png"];self.save()
        with self.assertRaisesRegex(ValueError,"指向包外"):self.check()

    def test_separate_vts_motion(self):
        p=self.pkg/"单次.motion3.json"
        with self.assertRaisesRegex(ValueError,"单次"):self.check(motions=[p.name])
        p.write_text('{"Version":3,"Meta":{"Duration":1,"Fps":60,"CurveCount":0,"TotalSegmentCount":0,"TotalPointCount":0},"Curves":[]}',encoding="utf-8")
        self.assertEqual(self.check(motions=[p.name])["checked_files"][-1]["file"],p.name)
        p.write_text('{"Version":',encoding="utf-8")
        with self.assertRaises(ValueError):self.check(motions=[p.name])


if __name__=="__main__":
    unittest.main()
