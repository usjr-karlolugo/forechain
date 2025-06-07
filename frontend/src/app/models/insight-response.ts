export interface InsightResponse {
    insight: string;
    impact_scale: 'Low' | 'Medium' | 'High';
    reasoning: string;
    recommendation: {
        summary: string;
        when: string;
        where: string;
        why: string;
        how: string[];
    };
}
