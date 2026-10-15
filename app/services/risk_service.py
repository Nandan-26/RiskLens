from datetime import datetime
from app.services.business_service import BusinessService
class RiskService:
    @staticmethod
    def evaluate_business_risk(business_id):
        b=BusinessService.get_business_by_id(business_id)
        if not b: return None
        score=0; rules=[]; year=datetime.now().year
        if not b.get('industry') or not b['industry'].strip():
            score+=20; rules.append({'rule':'Missing industry classification','impact':20})
        if not b.get('contact_email') or '@' not in b['contact_email']:
            score+=25; rules.append({'rule':'Missing or malformed email field','impact':25})
        if not b.get('founded_year'):
            score+=25; rules.append({'rule':'Missing foundation year','impact':25})
        elif b['founded_year']>year-2:
            score+=15; rules.append({'rule':'Recently founded','impact':15})
        score=min(100,score)
        tier='Low Risk Demo Tier' if score<=30 else 'Moderate Risk Demo Tier' if score<=65 else 'High Risk Demo Tier'
        return {'business_id':b['id'],'company_name':b['company_name'],'registration_number':b['registration_number'],'demo_risk_score':score,'demo_risk_tier':tier,'rules_evaluation':rules,'disclaimer':'Illustrative data-completeness score only; not verified business, credit, or compliance assessment.'}
