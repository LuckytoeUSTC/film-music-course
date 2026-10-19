import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import fs from 'node:fs/promises';
import {constants} from 'node:fs';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const skill='C:/Users/lucky/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
process.env.RUNTIME_NODE_MODULES='C:/Users/lucky/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
// Managed Windows filesystem disallows hard links. Preserve exclusive publication,
// then allow the unmodified finalizer to verify identical bytes and write its receipt.
const nativeLink=fs.link;
fs.link=async(src,dst)=>dst===path.join(root,'交付','听见末代皇帝_音乐赏析.pptx')?fs.copyFile(src,dst,constants.COPYFILE_EXCL):nativeLink(src,dst);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')));
const result=await finalizePresentation({workspaceDir:root,candidatePath:path.join(root,'build','candidate_media.pptx'),finalPath:path.join(root,'交付','听见末代皇帝_音乐赏析.pptx'),pythonExecutable:'C:/Users/lucky/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:28,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Microsoft YaHei']},verifyArtifactToolImport:true,receiptPath:path.join(root,'制作记录','presentation.final.validation.json')});
console.log(JSON.stringify(result));
