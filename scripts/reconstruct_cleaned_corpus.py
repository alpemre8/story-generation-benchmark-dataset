#!/usr/bin/env python3
"""Reconstruct the exact cleaned experimental corpus from a lawful local copy
of the historical STAGE_v0 script.json inputs.

This script does NOT download or redistribute screenplay text.
"""
import argparse, hashlib, json
from pathlib import Path

COMMIT = "ce4468eac15775a85e5cd3a2e7255d96ff1afb45"
RULES = {
"chasing_amy": ("en12839bdf037c46a0a3d9de0e50a6cbaa", 34, None, None, True, "ef03972add4a8c7fb77575424f5ca1c728a5d72fa2b2b91b4b2ba89a5395d34d"),
"ghostbusters_ii": ("enc76f658069e44354af1c5f8ab366d9ff", None, None, None, True, "c33bec4add0d90a5eebc7069f0290cf1f9ad2adfb2cdf8b986f9a031229627f5"),
"the_private_life_of_sherlock_holmes": ("en5a2464c851a44d5e814a92455b48783b", None, None, None, True, "9e2cd3f5555d153fffd8d7a84704b5a31a7b1cb7904d6046b1ff28cda49a7a10"),
"dog_day_afternoon": ("en140365ba66ff4e7481ff1a0b2b5e68e8", 69, "\nTHE END", None, False, "cd687208bd61d135886509a114ca3742c9576bcf6f2835f6129c94baf8a2bfb8"),
"apocalypse_now": ("en3b8f79aa09a045818b4e725fdf6b57e7", 60, "\nTHE END", None, False, "6a9fc5ef3907ac795bc0434b5fac5c8d905e7494a6440ce58b6511589aff0a64"),
"drag_me_to_hell": ("en17793caa790647fcb4e8ee9221a2a43a", None, None, None, False, "cbb7179864a0f79df7026397a9a3a0840a195ed756c74aaedbc5721dc2d548e4"),
"up_2009": ("ena1acdede6d524bffaf3a93bf0087206c", None, None, None, False, "c06f50d742f329d6381c5656ab7716caa88690ab49a8608736af88542e605918"),
"darkman": ("en7f8648f5449c4f9da46febfd68cdbd58", None, None, None, False, "0dc3a78c2568af23283328fd74d7b333462190243df4363533cdef1fc60d5c54"),
"do_the_right_thing": ("en97cd44f4ac92471e9137b4d2262a4dac", None, None, None, False, "3912c4b863b78c35044293f6377ce0b561108b848cee1a6feec75dadb65a86ed"),
"the_white_ribbon": ("en1ae8880bb21245a39ad18f119e163fec", None, None, "\n\n\tWhite Ribbon, The", False, "89b29fbe35b4af8ec4c0f374fa76d063873e6cae1099ae9b29d7f63b170432e6"),
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--stage-english-root', required=True, help='Path to the historical STAGE English directory')
    ap.add_argument('--output-root', required=True)
    args=ap.parse_args()
    src=Path(args.stage_english_root); out=Path(args.output_root); out.mkdir(parents=True,exist_ok=True)
    failed=[]
    for film,(sid,n,keep_marker,drop_marker,trailing_lf,expected) in RULES.items():
        p=src/sid/'script.json'
        data=json.loads(p.read_text(encoding='utf-8'))
        if n is not None: data=data[:n]
        if keep_marker:
            c=data[-1]['content']; i=c.find(keep_marker)
            if i < 0: raise RuntimeError(f'{film}: terminal marker not found')
            data[-1]['content']=c[:i+len(keep_marker)]
        if drop_marker:
            c=data[-1]['content']; i=c.find(drop_marker)
            if i < 0: raise RuntimeError(f'{film}: footer marker not found')
            data[-1]['content']=c[:i]
        text=json.dumps(data, ensure_ascii=False, indent=2) + ('\n' if trailing_lf else '')
        dst=out/film/'script.json'; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(text,encoding='utf-8',newline='')
        got=hashlib.sha256(dst.read_bytes()).hexdigest()
        ok=(got==expected)
        print(f'{film}: {"PASS" if ok else "FAIL"} sha256:{got}')
        if not ok: failed.append((film,expected,got))
    if failed:
        raise SystemExit('Hash verification failed for: '+', '.join(x[0] for x in failed))
    print('All 10 cleaned screenplay hashes match the experimental corpus.')

if __name__=='__main__': main()
