(function(){
var bg=document.getElementById('burger'),body=document.body;
if(bg){bg.addEventListener('click',function(){var o=body.classList.toggle('menu-open');bg.setAttribute('aria-expanded',o);bg.textContent=o?'Fechar':'Menu'});
document.querySelectorAll('.ov a').forEach(function(a){a.addEventListener('click',function(){body.classList.remove('menu-open');bg.setAttribute('aria-expanded',false);bg.textContent='Menu'})})}
var els=document.querySelectorAll('[data-r]');
if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('on')});return}
var io=new IntersectionObserver(function(es){var n=0;es.forEach(function(e){if(e.isIntersecting){e.target.style.transitionDelay=(Math.min(n++,4)*90)+'ms';e.target.classList.add('on');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
els.forEach(function(e){io.observe(e)});
})();
(function(){
var calm=matchMedia('(prefers-reduced-motion: reduce)').matches,vs=document.querySelectorAll('video[data-auto]');
if(calm){vs.forEach(function(v){v.controls=true;v.preload='metadata'});document.querySelectorAll('.vbtn').forEach(function(b){b.hidden=true});return}
if(!('IntersectionObserver' in window))return;
var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting&&!v.dataset.paused){var p=v.play();if(p)p.catch(function(){})}else v.pause()})},{rootMargin:'120px'});
vs.forEach(function(v){io.observe(v)});
document.querySelectorAll('.vbtn').forEach(function(b){var v=b.parentNode.querySelector('video');b.addEventListener('click',function(){if(v.paused){delete v.dataset.paused;v.play();b.textContent='Pausar'}else{v.dataset.paused='1';v.pause();b.textContent='Reproduzir'}})});
})();
(function(){
var h=document.querySelector('.hero'),hd=document.querySelector('.hd');
if(!h||!hd)return;
function u(){hd.classList.toggle('solid',scrollY>h.offsetHeight-hd.offsetHeight)}
addEventListener('scroll',u,{passive:true});addEventListener('resize',u);u();
})();
