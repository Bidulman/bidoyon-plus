window.onload = () => {
    let seconds = 15
    const pageInfo = document.getElementById('page-info')
    const baseText = pageInfo.innerHTML
    pageInfo.innerHTML = baseText + " (Rechargement dans " + seconds + " secondes)"
    setInterval(() => {
        if (seconds > 0) {
            seconds -= 1
            pageInfo.innerHTML = baseText + " (Rechargement dans " + seconds + " secondes)"
        } else {
            location.reload()
        }
    }, 1000)
}