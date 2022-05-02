/**
 * Parse bom.gov.au station list
 * 
 * Execude the following code in your browser's console on any of the sites
 * mentioned in the "Observations - individual stations" section
 * on http://www.bom.gov.au/catalogue/data-feeds.shtml
 * (e.g. http://www.bom.gov.au/nsw/observations/nswall.shtml)
 */

const base = "http://www.bom.gov.au";
const links = document.getElementsByTagName("a");
const stations = Array.from(links)
  .filter((link) => link.href.startsWith(`${base}/products/ID`))
  .map((link) => link.href.replace(`${base}/products/`, "").replace("shtml", "json"));
console.log(JSON.stringify(stations));