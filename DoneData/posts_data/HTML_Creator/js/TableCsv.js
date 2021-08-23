export default class {
    /**
     *
     * @param {HTMLTableElement} root The table element which will display the CSV data.
     */
    constructor(root) {
        this.root = root;
        console.log("I'm constructed.")
    }

    /**
     *
     * @param {string[][]} data A 2D array of data to be used as the table body.
     * @param {string[]} headerColumns List of heading to be used.
     */
    update(data, headerColumns = []) {
        this.clear();
        this.setHeader(headerColumns);
        this.setBody(data);
    }

    /**
     * Clear all the contents of table (incl. the header).
     */
    clear() {
        this.root.innerHTML = "";
    }

    /**
     *
     * @param {string[]} headerColumns List of heading to be used.
     */
    setHeader(headerColumns) {
        this.root.insertAdjacentHTML("afterbegin", `
            <thead>
                <tr>
                    <th>image_of_post</th>
                    ${ headerColumns.map(text => `<th>${text}</th>`).join("") }
                </tr>
            </thead>
        `)
    }

    /**
     *
     * @param {string[][]} data A 2D array of data to be used as the table body.
     */
    setBody(data) {
        const rowsHtml = data.map(row => {
            let id = row[0]
            id = id.replace("https://www.instagram.com/p/", "")
            id = id.replace("/", "")
            let image_location = "data/marry_posts/images/" + id + ".jpg"
            return `
                <tr>
                    <td>
                         <img src=${ image_location } alt=${ id }>
                    </td>
                    ${ row.map(text => `<td>${ text }</td>` ).join("") }
                </tr>
            `;
        });

        this.root.insertAdjacentHTML("beforeend", `
            <tbody>
                ${ rowsHtml.join("") }
            </tbody>
    `);
    }
}