import TableCsv from "./TableCsv.js";

const tableRoot = document.querySelector("#csvRoot");
const csvFileInput = document.querySelector("#csvFileInput");
const tableCsv = new TableCsv(tableRoot);

csvFileInput.addEventListener("change", e => {
    // console.log(csvFileInput.files[0]);

    Papa.parse(csvFileInput.files[0], {
        delimiter: ",",
        skipEmptyLines: true,
        complete: results => {
            console.log(results)
            // console.log(results)
            tableCsv.update(results.data.slice(1), results.data[0]);
        }
    });
});

// let header = ["ID", "Name", "Age"]
// let body = [
//     [ 1, "Foo", 1],
//     [ 2, "Bar", 2],
//     [ 12, "Foobar", 12],
// ]
// tableCsv.setHeader(header)
// tableCsv.setBody(body)

// tableCsv.update(body, header)
