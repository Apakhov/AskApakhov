$(document).ready(function(){
    var colors = ['#CFA3FF', '#559900', '#28A22C', '#131506']
    var tags = ['perl', 'python', 'TechnoPark', 'MySQL', 'django', 'Mail.Ru', 'Voloshin', 'Firefox'];

    var $tag_cloud = $('#tag-cloud');
    tags.forEach((value) => {
        var newTag = document.createElement('a');
    
        newTag.classList.add('m-1');
        newTag.style.display = 'inline-block';
        newTag.style.color = colors[Math.floor(Math.random() * 4)];
        newTag.style.fontSize = (Math.floor(Math.random() * 18) + 12).toString() + 'px';

        newTag.href = '/tag/' + value;
        newTag.innerText = value;

        $tag_cloud.append(newTag);
    })
});