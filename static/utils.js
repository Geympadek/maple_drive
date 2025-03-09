/**
 * @param {String} HTML representing any number of sibling nodes
 * @return {NodeList} 
 */
function html_to_nodes(html) {
    html = html.trim()
    const template = document.createElement('template');
    template.innerHTML = html;
    return template.content.childNodes;
}
/**
 * @param {String} HTML representing a single node (which might be an Element,
                   a text node, or a comment).
 * @return {Node}
 */
function html_to_node(html)
{
    return html_to_nodes(html)[0]
}