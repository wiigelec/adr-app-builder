#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; PROFILES=ROOT/"product"/"src"/"profiles"; DEFAULT_ADR_REPOSITORY="https://github.com/wiigelec/adr.git"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def obj(n,v):
    if not isinstance(v,dict): raise SystemExit(f"{n} must be a JSON object")
def string(n,v):
    if not isinstance(v,str) or not v: raise SystemExit(f"{n} must be a non-empty string")
def resolve_adr_main(repo):
    p=subprocess.run(["git","ls-remote",repo,"refs/heads/main"],text=True,capture_output=True)
    if p.returncode: raise SystemExit("unable to resolve ADR main: "+p.stderr.strip())
    parts=p.stdout.strip().split();
    if not parts: raise SystemExit("ADR main did not resolve")
    return parts[0]
def builder_commit():
    dirty=subprocess.run(["git","status","--porcelain","--","product/src/app_builder.py"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    if dirty: raise SystemExit("builder implementation has uncommitted changes; commit it before building")
    return subprocess.run(["git","log","-1","--format=%H","--","product/src/app_builder.py"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
def profile(pid):
    p=PROFILES/f"{pid}.json"
    if not p.is_file(): raise SystemExit(f"unknown profile: {pid}")
    return load(p)
def validate_sources(app,rules,dataset,build):
    for n,v in [("application",app),("ruleset",rules),("dataset",dataset),("build",build)]: obj(n,v)
    string("application.id",app.get("id")); obj("application.initialization",app.get("initialization"))
    ins=app["initialization"].get("instructions")
    if not isinstance(ins,list) or not ins or not all(isinstance(x,str) and x for x in ins): raise SystemExit("application.initialization.instructions must be a non-empty string list")
    obj("dataset.instance",dataset.get("instance")); string("dataset.instance.id",dataset["instance"].get("id")); string("build.packaging_profile",build.get("packaging_profile"))
    ps=build.get("providers")
    if not isinstance(ps,list) or not ps or not all(isinstance(x,str) and x for x in ps) or len(set(ps))!=len(ps): raise SystemExit("build.providers must be a non-empty unique string list")
def main():
    ap=argparse.ArgumentParser();
    for a in ["application","ruleset","dataset","build"]: ap.add_argument(f"--{a}",required=True,type=Path)
    ap.add_argument("--output-dir",required=True,type=Path); ap.add_argument("--adr-repository",default=DEFAULT_ADR_REPOSITORY); args=ap.parse_args()
    app,rules,dataset,build=[load(getattr(args,x)) for x in ["application","ruleset","dataset","build"]]; validate_sources(app,rules,dataset,build)
    packaging=profile(build["packaging_profile"]); obj("packaging.preservation",packaging.get("preservation"))
    if packaging.get("id")!=build["packaging_profile"] or packaging["preservation"].get("writeback")!="complete-realization" or packaging["preservation"].get("preserve_non_dataset_realization_material") is not True: raise SystemExit("invalid FS-001 packaging profile")
    adr=resolve_adr_main(args.adr_repository); bc=builder_commit()
    for pid in build["providers"]:
        provider=profile(pid); obj("provider.bootstrap",provider.get("bootstrap"))
        if provider.get("id")!=pid or provider["bootstrap"].get("mode")!="initialize" or not provider["bootstrap"].get("instructions"): raise SystemExit(f"invalid provider profile: {pid}")
        artifact={"adr_realization":{"format":packaging["format"],"format_version":packaging["format_version"],"provenance":{"adr_commit":adr,"app_builder_commit":bc},"authority":{"generated_realization_is_normative":False,"dataset_is_authoritative_for_committed_application_state":True},"provider":{"profile":pid,"name":provider["provider"]},"application":app,"initialization":{"application":app["initialization"],"provider":provider["bootstrap"]},"ruleset":rules,"dataset":dataset,"preservation":packaging["preservation"]}}
        out=args.output_dir/f"{pid}.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(artifact,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__": main()
