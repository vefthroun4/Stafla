import { DataFetcher } from "../datafetcher.js";

class Ancestors extends DataFetcher {
    constructor(submit, elems=null) {
        super()
        this.tree = {}
        this.elems = elems
        this.submit = submit
        
        if (elems) {
            this.set_ancestors()
            this.set_eventlisteners()
            this.fix_startup()
        }
    }

    set_ancestors() {        
        for(let i = 0; i < this.elems.length; i++) {
            this.tree[this.elems[i].name] = {}
            this.tree[this.elems[i].name]["children"] = []
            this.tree[this.elems[i].name]["parent"] = this.elems[i]
            for (let j = i+1; j < this.elems.length; j++) {
                this.tree[this.elems[i].name]["children"].push(this.elems[j])
            }
        }
    }

    set_eventlisteners() {
        // computes stuff
        for (const [resource, entity] of Object.entries(this.tree)) {
            if (entity.children.length) {
                let parent = entity.parent
                let child = entity.children[0]

                parent.addEventListener("change", (e) => {
                    entity.children.map(child => {
                        // purge the child
                        this.purge_options(child)
                    }) 
                    
                    if (e.target.value) { 
                        this.set_select_data(parent,child)
                    }

                })
            }
        }
    }

    set_select_data(parent, child) {
        this.get_data(parent.name+"s", parent.value).then(data => {
            if (data && child.name+"s" in data) {
                this.create_options(child, data[child.name+"s"], {"id": child.name+"ID", "name": child.name+"_name"})
                child.disabled=false
            }
        }) 
    }

    fix_startup() {
        "Meant to run on startup on the uppermost tree element"
        let treeElem = this.tree[Object.keys(this.tree)[0]]
        if (treeElem.parent.value && treeElem.parent.value !== "__None") {
            this.set_select_data(treeElem.parent, treeElem.children[0])
        }
        treeElem.parent.disabled=false
    }

    purge_options(parent) {
        const nodes = parent.childNodes
        for (let i = nodes.length-1; i > 0; i--) {
            nodes[i].remove()
        } 
        parent.disabled = true      
    }

    create_options(parent, children, keys) {
        let fragment = new DocumentFragment()
        children.map(child => {
            let option = document.createElement("option")
            option.value = child[keys.id]
            option.name = child[keys.name]
            option.text = child[keys.name]
            fragment.appendChild(option)
        }) 
        parent.appendChild(fragment)
    }
}
let anc = new Ancestors(document.querySelector("input[type='submit']"), document.querySelectorAll("select"))


    



