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
                        this.get_data(parent.name+"s", parent.value).then(data => {
                            if (data && child.name+"s" in data) {
                                this.create_options(child, data[child.name+"s"], {"id": child.name+"ID", "name": child.name+"_name"})
                                child.disabled=false
                            }
                        }) 
                    }

                })
            }
        }
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



// Quick fix for when submitting form and resetting school value
let sc = document.querySelector("[name='school']")
if (sc.value) {
    sc.value = ""
}
sc.disabled=false
    
    



