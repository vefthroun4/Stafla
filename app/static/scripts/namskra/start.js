import { DataFetcher } from "../datafetcher.js";

class Ancestors extends DataFetcher {
    constructor(submit, elems=null) {
        super()
        this.tree = {}
        this.state = {}
        this.elems = elems
        this.submit = submit
        if (elems) {
            this.set_ancestors()
            this.set_eventlisteners()
            this.fix_startup()
            this.setup_state()
        }
    }

    setup_state() {
        // Invoke only after tree has been setup.
        for (const[elem, entity] of Object.entries(this.tree)) {
            this.state[elem] = false
        }
    }

    update_state(parent) {
        if (parent.value) {
            this.state[parent.name] = true
        }
        if (Object.values(this.state).every(x => x === true)) {
            this.submit.disabled = false
        } else {
            this.submit.disabled = true
        }

    }

    reset_state(parent) {
        if (!parent.value) {
            this.state[parent.name] = false
        }

        // reset child states
        if (this.tree[parent.name].children) {
            this.tree[parent.name].children.map(child => {
                this.state[child.name] = false
            })
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
            let parent = entity.parent
            let child = entity.children[0]
            parent.addEventListener("change", (e) => {
                entity.children.map(child => {
                    // purge the child
                    this.purge_options(child)
                }) 

                // Resets state of childrens parents
                this.reset_state(parent)

                // Updates state of parent
                this.update_state(parent)

                // Makes a request to api for data and appends options under the child's select
                if (e.target.value && child) { 
                    let result = this.set_select_data(parent,child)
                    if (!result) {
                        // Revokes state change if api didn't return result
                        this.reset_state(parent)
                    } 
                    
                }
            })
        }
    }
    
    // Set to async in case api is unable to return data 
    async set_select_data(parent, child) {
        await this.get_data(parent.name+"s", parent.value).then(data => {
            if (data && child.name+"s" in data) {
                this.create_options(child, data[child.name+"s"], {"id": child.name+"ID", "name": child.name+"_name"})
                child.disabled=false
                return true
            }
            return false
        }) 
    }

    fix_startup() {
        "Meant to run on startup on the uppermost tree element"
        let treeElem = this.tree[Object.keys(this.tree)[0]]
        console.log(treeElem.parent.value)
        if (treeElem.parent.value !== "__None") {
            this.set_select_data(treeElem.parent, treeElem.children[0])
            console.log("hm")
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

    



