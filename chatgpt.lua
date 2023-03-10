local prompt = "Rewrite the following text. Aim for clarity and succinctness. Avoid wordiness. It should sound professional but light.\n\n"

-- Put your OpenAI API key in ~/.openai_key
function getKey()
    local home = os.getenv("HOME")
    local file = io.open(home .. "/.openai_key", "r")
    local contents = file:read("*all")
    file:close()
    return contents
end

function chatGpt(text, key, callback)
    local headers = {
        ["Content-Type"] = "application/json",
        ["Authorization"] = "Bearer " .. key,
    }
    local post = {
        model = "gpt-3.5-turbo",
        messages = {
            { role = "system", content = "You are a helpful assistant." },
            { role = "user", content = text }
        }
    }
    local postData = hs.json.encode(post)

    hs.http.asyncPost("https://api.openai.com/v1/chat/completions", postData, headers, callback)
end

function getSelectedText()
    local element = hs.uielement.focusedElement()
    if element then
        return element:selectedText()
    end
end

 function trim(s)
   return s:gsub("^%s*(.-)%s*$", "%1")
 end

-- Invoke API on key binding
hs.hotkey.bind({ "cmd" }, "f1", function()
    local text = trim(getSelectedText())
    if text and string.len(text) > 0 then
        print("\"" .. text .. "\"")
        print(string.len(text) > 0)
        chatGpt(prompt .. text, getKey(),function(_, body, _)
            hs.eventtap.keyStroke({}, "delete")
            hs.eventtap.keyStrokes(hs.json.decode(body)["choices"][1]["message"]["content"])
        end)
    else
        hs.notify.new({ title = "Error", informativeText = "No text selected" }):send()
    end
end)