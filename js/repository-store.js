import { Utils } from './utils.js';
export class RepositoryStore{
 constructor(data){this.data=data;this.resources=this.flatten(data.sections);this.cache=new Map();}
 flatten(sections){return sections.flatMap(s=>s.categories.flatMap(c=>c.resources.map(r=>({...r,sectionId:s.id,sectionName:s.name,sectionIcon:s.icon,sectionDescription:s.description,categoryId:c.id,categoryName:c.name,categoryDescription:c.description}))));}
 getTypes(){return [...new Set(this.resources.map(x=>x.type))].sort((a,b)=>a.localeCompare(b,'es'));}
 getById(id){return this.resources.find(x=>x.id===id);}
 async load(resource){if(this.cache.has(resource.id))return this.cache.get(resource.id);const response=await fetch(encodeURI(resource.virtualPath),{cache:'no-cache'});if(!response.ok)throw new Error(`No se pudo cargar ${resource.virtualPath} (${response.status})`);const text=await response.text();this.cache.set(resource.id,text);return text;}
 query({text='',section='all',type='all'}={}){const q=Utils.normalize(text);return this.resources.filter(x=>{if(section!=='all'&&x.sectionId!==section)return false;if(type!=='all'&&x.type!==type)return false;if(!q)return true;return Utils.normalize([x.title,x.summary,x.virtualPath,x.type,x.sectionName,x.categoryName,(x.tags||[]).join(' ')].join(' ')).includes(q);});}
 group(resources){return this.data.sections.map(s=>({...s,categories:s.categories.map(c=>({...c,resources:resources.filter(x=>x.sectionId===s.id&&x.categoryId===c.id)})).filter(c=>c.resources.length)})).filter(s=>s.categories.length);}
 stats(){return{sections:this.data.sections.length,categories:this.data.sections.reduce((a,s)=>a+s.categories.length,0),resources:this.resources.length,types:this.getTypes().length};}
}
