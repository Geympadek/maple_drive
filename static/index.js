const EXPLORER = document.querySelector("#explorer")

const FILE_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19.949,5.536,16.465,2.05A6.958,6.958,0,0,0,11.515,0H7A5.006,5.006,0,0,0,2,5V19a5.006,5.006,0,0,0,5,5H17a5.006,5.006,0,0,0,5-5V10.485A6.951,6.951,0,0,0,19.949,5.536ZM18.535,6.95A4.983,4.983,0,0,1,19.316,8H15a1,1,0,0,1-1-1V2.684a5.01,5.01,0,0,1,1.051.78ZM20,19a3,3,0,0,1-3,3H7a3,3,0,0,1-3-3V5A3,3,0,0,1,7,2h4.515c.164,0,.323.032.485.047V7a3,3,0,0,0,3,3h4.953c.015.162.047.32.047.485Z"/></svg>'
const FOLDER_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m23.493,11.017c-.487-.654-1.234-1.03-2.05-1.03h-.443v-1.987c0-2.757-2.243-5-5-5h-5.056c-.154,0-.31-.037-.447-.105l-3.155-1.578c-.414-.207-.878-.316-1.342-.316h-2C1.794,1,0,2.794,0,5v13c0,2.757,2.243,5,5,5h12.558c2.226,0,4.15-1.432,4.802-3.607l1.532-6.116c.234-.782.089-1.605-.398-2.26ZM2,18V5c0-1.103.897-2,2-2h2c.154,0,.31.037.447.105l3.155,1.578c.414.207.878.316,1.342.316h5.056c1.654,0,3,1.346,3,3v1.987h-10.385c-1.7,0-3.218,1.079-3.789,2.72l-2.19,7.138c-.398-.509-.636-1.15-.636-1.845Zm19.964-5.253l-1.532,6.115c-.384,1.279-1.539,2.138-2.874,2.138H5c-.208,0-.411-.021-.607-.062l2.334-7.609c.279-.803,1.039-1.342,1.889-1.342h12.828c.242,0,.383.14.445.224.062.084.156.259.075.536Z"/></svg>'

let current_folder = "."

async function file_to_html(info)
{
    let el = document.createElement("div")
    
    let icon = null

    let label = document.createElement('p')
    label.innerHTML = info.name

    if (info.type == "file")
    {
        el.className = "file"
        icon = FILE_ICON
    }
    else
    {
        el.className = "folder"
        icon = FOLDER_ICON
    }
    el.innerHTML += icon
    el.appendChild(label)
    return el
}

async function display_dir(dir_path)
{
    

    const response = await fetch(`/api/list_dir?path=${dir_path}`, {
        method: "GET",
        credentials: "include"
    })

    EXPLORER.innerHTML = ""

    let contents = await response.json()

    for (let file_info of contents)
    {
        let el = await file_to_html(file_info)
        EXPLORER.appendChild(el)
    }
}

document.addEventListener("auth_complete", () => {
    console.log("yey you authorized!!!")
    display_dir(current_folder)
})