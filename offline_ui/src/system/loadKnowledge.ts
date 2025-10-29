export type CriderBrainType = any;

export async function loadKnowledge(): Promise<CriderBrainType> {
  try {
    const res = await fetch('/knowledge/knowledge.json', { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch knowledge.json');
    const data = await res.json();
    const CriderBrain = Object.freeze(data);
    console.log('🧠 CriderGPT Brain Loaded Successfully.');
    return CriderBrain;
  } catch (err) {
    console.error('Failed to load knowledge:', err);
    const empty = Object.freeze({});
    return empty;
  }
}
