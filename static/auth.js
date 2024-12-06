class AuthError extends Error
{
    constructor(msg, options)
    {
        super(msg, options)
    }
}

async function auth()
{
    data_str = window.Telegram.WebApp.initData
    if (data_str == undefined)
    {
        throw new AuthError("No Telegram data provided.")
    }

    const response = await fetch('/api/auth', {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: data_str
    })
    console.log(await response.json())
}
auth()