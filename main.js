const fs = require("fs");
const path = require("path");
const AdmZip = require("adm-zip");
require("./build");
require("./slides");
const { pres } = require("./build");

const finalPath = "D:\\pptx-build\\mcluhan-makaleh.pptx";

(async () => {
  const buf = await pres.write({ outputType: "nodebuffer" });
  const zip = new AdmZip(Buffer.from(buf));

  const transitionXml = '<p:transition spd="med"><p:fade/></p:transition>';
  for (let i = 1; i <= 30; i++) {
    const entry = zip.getEntry(`ppt/slides/slide${i}.xml`);
    if (!entry) continue;
    let xml = entry.getData().toString("utf8");
    xml = xml.replace(/<p:transition[^>]*>.*?<\/p:transition>/s, "");
    if (xml.includes("<p:timing>")) {
      xml = xml.replace("<p:timing>", transitionXml + "<p:timing>");
    } else if (xml.includes("</p:sld>")) {
      xml = xml.replace("</p:sld>", transitionXml + "</p:sld>");
    }
    zip.updateFile(`ppt/slides/slide${i}.xml`, Buffer.from(xml, "utf8"));
  }

  const outBuf = zip.toBuffer();
  fs.writeFileSync(finalPath, outBuf);
  console.log("Written:", finalPath, outBuf.length, "bytes");
})().catch(e => { console.error("FATAL:", e); process.exit(1); });
