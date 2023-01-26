import Fuse from './fuse.esm.js';

const templater = document.createElement('template');
templater.innerHTML = `
<style>
@import "/static/bootstrap-5.2.0/dist/css/bootstrap.rtl.min.css";
@import "/static/fontawesome-free-6.2.1-web/css/all.css";
button{
    width: 100px
}
th{
    cursor:pointer 
}
</style>
`;

class DataTabler extends HTMLElement {
    constructor() {
        super();

        if (this.hasAttribute('src')) this.src = this.getAttribute('src');
        // If no source, do nothing
        if (!this.src) return;

        // attributes to do, datakey
        if (this.hasAttribute('cols'))
            this.cols = this.getAttribute('cols').split(',');

        this.pageSize = 10;
        if (this.hasAttribute('pagesize'))
            this.pageSize = this.getAttribute('pagesize');

        // helper values for sorting and paging
        this.sortAsc = false;
        this.curPage = 1;
        this.df = [];
        const shadow = this.attachShadow({
            mode: 'open',
        });
        this.shadowRoot.appendChild(templater.content.cloneNode(true));
        const div1 = document.createElement('div');
        const table = document.createElement('table');
        table.classList.add('table', 'table-striped');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');
        tbody.classList.add('table-group-divider');
        const input = document.createElement('input');
        input.classList.add('form-control');
        const i = document.createElement('i');
        i.classList.add('fa-sharp', 'fa-solid', 'fa-magnifying-glass');
        table.append(thead, tbody);

        const nav = document.createElement('div');
        const prevButton = document.createElement('button');
        prevButton.classList.add('btn', 'btn-outline-secondary');
        prevButton.innerHTML = 'Previous';
        const nextButton = document.createElement('button');
        nextButton.classList.add('btn', 'btn-outline-secondary', 'mx-2');
        nextButton.innerHTML = 'Next';
        nav.append(prevButton, nextButton);

        const div2 = document.createElement('div');
        div2.classList.add('input-group', 'mb-3');
        const span = document.createElement('span');
        span.classList.add('input-group-text');

        span.append(i);

        div2.append(span, input);

        div1.append(div2, table);

        shadow.append(div1, nav);

        // Attach the created elements to the shadow dom

        // https://www.freecodecamp.org/news/this-is-why-we-need-to-bind-event-handlers-in-class-components-in-react-f7ea1a6f93eb/
        this.sort = this.sort.bind(this);

        this.nextPage = this.nextPage.bind(this);
        this.previousPage = this.previousPage.bind(this);
        this.search = this.search.bind(this);

        nextButton.addEventListener('click', this.nextPage, false);
        prevButton.addEventListener('click', this.previousPage, false);
    }

    load() {
        // error handling needs to be done :|
        this.data = JSON.parse(this.src);
        this.df = this.data;
        this.render();
    }

    nextPage() {
        if (this.curPage * this.pageSize < this.data.length) this.curPage++;
        this.renderBody();
    }

    previousPage() {
        if (this.curPage > 1) this.curPage--;
        this.renderBody();
    }

    render() {
        if (!this.cols) this.cols = Object.keys(this.data[0]['fields']);

        this.renderHeader();
        this.renderBody();
    }

    renderBody() {
        let result = '';
        this.data
            .filter((row, index) => {
                let start = (this.curPage - 1) * this.pageSize;
                let end = this.curPage * this.pageSize;
                if (index >= start && index < end) return true;
            })
            .forEach((c) => {
                let r = '<tr>';
                r += `<td>${c['pk']}</td>`;
                this.cols.forEach((col) => {
                    r += `<td>${c['fields'][col] ? c['fields'][col] : ''}</td>`;
                });
                r += '</tr>';
                result += r;
            });

        let tbody = this.shadowRoot.querySelector('tbody');
        tbody.innerHTML = result;
    }

    renderHeader() {
        let header = '<tr>';
        header += `<th scope='col' data-sort="id">#</th>`;
        header += `<th scope='col' data-sort="name">الاسم</th>`;
        header += `<th scope='col' data-sort="fatherName">اسم الأب</th>`;
        header += `<th scope='col' data-sort="motherName">اسم الأم</th>`;
        header += `<th scope='col' data-sort="college">الكلية</th>`;
        header += '</tr>';
        let thead = this.shadowRoot.querySelector('thead');
        thead.innerHTML = header;

        this.shadowRoot.querySelectorAll('thead tr th').forEach((t) => {
            t.addEventListener('click', this.sort, false);
        });
        this.shadowRoot
            .querySelector('input')
            .addEventListener('input', this.search, false);
    }

    search(e) {
        const options = {
            includeScore: true,
            keys: ['fields.name'],
        };

        const fuse = new Fuse(this.data, options);

        const result = fuse.search(e.target.value);
        this.data = result.map((r) => r.item);
        if (!e.target.value) {
            this.data = this.df;
        }
        this.renderBody();
    }

    async sort(e) {
        let thisSort = e.target.dataset.sort;
        console.log('sort by', thisSort);

        if (this.sortCol && this.sortCol === thisSort)
            this.sortAsc = !this.sortAsc;
        this.sortCol = thisSort;
        if (this.sortCol === 'id') {
            this.data.sort((a, b) => {
                if (a['pk'] < b['pk']) return this.sortAsc ? 1 : -1;
                if (a['pk'] > b['pk']) return this.sortAsc ? -1 : 1;
                return 0;
            });
        } else {
            this.data.sort((a, b) => {
                if (a['fields'][this.sortCol] < b['fields'][this.sortCol])
                    return this.sortAsc ? 1 : -1;
                if (a['fields'][this.sortCol] > b['fields'][this.sortCol])
                    return this.sortAsc ? -1 : 1;
                return 0;
            });
        }

        this.renderBody();
    }

    static get observedAttributes() {
        return ['src'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
        // even though we only listen to src, be sure
        if (name === 'src') {
            this.src = newValue;
            this.load();
        }
    }
}

// Define the new element
customElements.define('data-table', DataTabler);
