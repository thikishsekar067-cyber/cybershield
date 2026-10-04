export type Analysis={riskLevel:'LOW'|'MEDIUM'|'HIGH';riskScore:number;confidence:string;classification:string;summary:string;indicators:string[];explanation:string;recommendedActions:string[]};
const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000';
export async function analyze(kind:string,payload:Record<string,unknown>):Promise<Analysis>{const r=await fetch(`${API}/api/analyze/${kind}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!r.ok)throw new Error('Analysis service unavailable');return r.json()}
