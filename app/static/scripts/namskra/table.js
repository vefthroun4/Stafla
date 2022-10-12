import { DataFetcher } from "../datafetcher.js"
import "../../node_modules/gridjs/dist/gridjs.umd.js"
new gridjs.Grid()


let df = new DataFetcher()
df.get_table_data_all().then(resp => {
    console.log(resp)
})

df.get_table_data_active().then(resp => {
    console.log(resp)
})