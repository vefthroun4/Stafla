"use strict"

export class DataFetcher {
    constructor() {
    }

    async get_table_data_all() {
        let resp = await fetch(window.origin+`/api/table/all`).then(resp => {
            return resp.json()
        }).then(data => {
            return data
        }).catch(err => {
            console.log(`Error occured: ${err}\n(ﾉ*ФωФ)ﾉ`)
            return false
        })
        return resp
    }

    async get_table_data_active() {
        let resp = await fetch(window.origin+`/api/table/active`).then(resp => {
            return resp.json()
        }).then(data => {
            return data
        }).catch(err => {
            console.log(`Error occured: ${err}\n(ﾉ*ФωФ)ﾉ`)
            return false
        })
        return resp
    }

    async get_data(resource, identifier) {
        let resp = await fetch(window.origin+`/api/${resource}/${identifier}`).then(resp => {
            return resp.json()
        }).then(data => {
            return data
        }).catch(err => {
            console.log(`Error occured: ${err}\n(ﾉ*ФωФ)ﾉ`)
        })
        return resp
    }

    async get_schools() {
        let resp = await fetch(window.origin+"/api/schools").then(resp => {
            return resp.json()
        }).then(school_data => {
            return school_data
        }).catch(err => {
            console.log(`Error occured: ${err}\n(ﾉ*ФωФ)ﾉ`)
        })
        return resp
    }
    
    async get_school(identifier) { 
        let resp = await fetch(window.origin+`/api/schools/${identifier}`).then(resp => {
            return resp.json()
        }).then(school_data => {
            return school_data
        }).catch(err => {
            console.log(`Error occured: ${err}\n(ﾉ*ФωФ)ﾉ`)
        })
        return resp
    }

    async get_division(identifier) { 
        let resp = await fetch(window.origin+`/api/divisions/${identifier}`).then(resp => {
            return resp.json()
        }).then(division_data => {
            return division_data
        }).catch(err => {
            console.log(`Error occured: ${err}\n(ﾉ*ФωФ)ﾉ`)
        })
        return resp
    }

    async get_track(identifier) { 
        let resp = await fetch(window.origin+`/api/tracks/${identifier}`).then(resp => {
            return resp.json()
        }).then(track_data => {
            return track_data
        }).catch(err => {
            console.log(`Error occured: ${err}\n(ﾉ*ФωФ)ﾉ`)
        })
        return resp
    }
}


