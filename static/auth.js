class AuthError extends Error
{
    constructor(msg, options)
    {
        super(msg, options)
    }
}

async function register()
{
    data_str = window.Telegram.WebApp.initData
    if (data_str == undefined)
        throw new AuthError("No Telegram data provided.")
    
    const response = await fetch(`/api/register?${data_str}`, {
        method: "POST"
    })
    if (!response.ok)
    {
        data = await response.json()

        if (data["type"] == "UserAlreadyExistsError")
            throw new AuthError(data["message"])
    }
}

async function auth()
{
    data_str = window.Telegram.WebApp.initData
    if (data_str == undefined)
        throw new AuthError("No Telegram data provided.")

    const response = await fetch(`/api/auth?${data_str}`, {
        method: "GET"
    })
    if (!response.ok)
    {
        data = await response.json()

        if (data["type"] == "UserNotFoundError")
            await register()
        else
            throw new AuthError(data["message"])
    }
    document.dispatchEvent(new Event("auth_complete"))
}

auth()