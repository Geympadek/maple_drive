const ADDRESS_BAR = document.querySelector("#address")
const EXPLORER = document.querySelector("#explorer")

current_path = ""

ADDR_SEP_EL = document.createElement("div")
ADDR_SEP_EL.className = "addr_sep"
ADDR_SEP_EL.textContent = ">"

function addr_folder_el(name)
{
    const div = document.createElement('div');
    div.className = 'addr_dir';
    div.textContent = name; // Set the text content to the name

    div.addEventListener('click', async () => {
        let idx = current_path.lastIndexOf(name)
        if (idx != -1)
            idx += name.length + 1
        new_path = current_path.substring(0, idx)
        
        await change_directory(new_path)
    })
    return div;
}

function update_address_bar()
{
    directories = current_path.split('/')
    ADDRESS_BAR.innerHTML = ""

    ADDRESS_BAR.appendChild(addr_folder_el("Drive"));
    ADDRESS_BAR.appendChild(ADDR_SEP_EL.cloneNode(true)); // Append a clone of the separator element

    directories.forEach(element => {
        if (element == "")
            return

        ADDRESS_BAR.appendChild(addr_folder_el(element));
        ADDRESS_BAR.appendChild(ADDR_SEP_EL.cloneNode(true));
    }); 
}

async function change_directory(path)
{
    current_path = path
    update_address_bar()
    await update_files_list()
}

function visualize_file(file)
{
    result = document.createElement("div")
    
    if (file['is_file'])
    {
        result.className = "file"
        result.appendChild(FILE_ICON.cloneNode(true))
    }
    else
    {
        result.className = "folder"
        result.appendChild(DIR_ICON.cloneNode(true))
        result.addEventListener('click', () => {return change_directory(current_path + `${file["filename"]}/`)})
    }

    desc = document.createElement('div')
    desc.className = "desc"

    filename = document.createElement('p')
    filename.className = "filename"
    filename.textContent = file["filename"]
    desc.appendChild(filename)

    file_button = document.createElement('div')
    file_button.textContent = "⋮"
    desc.appendChild(file_button)

    result.appendChild(desc)

    return result
}

async function update_files_list()
{
    const response = await fetch(`/api/list?path="${current_path}"`, {
        method: "GET",
        credentials: "include"
    })
    data = await response.json()

    EXPLORER.innerHTML = ""
    data.forEach(file => {
        EXPLORER.appendChild(visualize_file(file))
    });
}

document.addEventListener("auth_complete", async () => {
    console.log("yey you authorized!!!")
    update_address_bar()
    await update_files_list()
})