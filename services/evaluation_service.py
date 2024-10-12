from models.interview_questions import get_questions

def evaluate_transcript_with_questions(transcript):
    """Transkripti sorularla eşleştirip uygunluk skorları döner"""
    questions = get_questions()
    evaluation_results = []
    
    for question in questions:
        if question.lower() in transcript.lower():
            score = 1  # Basit bir uygunluk kontrolü
        else:
            score = 0
        
        evaluation_results.append({
            "question": question,
            "matched": score
        })
    
    return evaluation_results

def evaluate_gestures(gesture_data):
    """Jest ve mimik sonuçlarını değerlendirir"""
    scores = []
    
    for gesture in gesture_data:
        eye_openness = gesture["eye_openness"]
        mouth_openness = gesture["mouth_openness"]
        
        # Basit bir değerlendirme: Göz açıklığı ve ağız hareketine göre değerlendirme
        if eye_openness > 0.05 and mouth_openness > 0.05:
            score = 1  # Normal
        else:
            score = 0  # Şüpheli veya anormal jest
        
        scores.append(score)
    
    overall_score = sum(scores) / len(scores) if scores else 0
    return overall_score

def evaluate_interview(transcript, gesture_data):
    """Tüm değerlendirmeleri birleştirir"""
    transcript_evaluation = evaluate_transcript_with_questions(transcript)
    gesture_score = evaluate_gestures(gesture_data)
    
    final_score = (sum([result['matched'] for result in transcript_evaluation]) + gesture_score) / (len(transcript_evaluation) + 1)
    
    return {
        "transcript_evaluation": transcript_evaluation,
        "gesture_score": gesture_score,
        "final_score": final_score
    }
import spacy
from models.interview_questions import get_questions

# SpaCy dil modeli
nlp = spacy.load('en_core_web_lg')

def evaluate_transcript_with_questions(transcript):
    """Transkripti sorularla eşleştirip NLP ile benzerlik skorları döner"""
    questions = get_questions()
    evaluation_results = []
    
    # Transkriptin NLP nesnesi haline getirilmesi
    transcript_doc = nlp(transcript)

    for question in questions:
        question_doc = nlp(question)
        similarity_score = transcript_doc.similarity(question_doc)
        
        evaluation_results.append({
            "question": question,
            "similarity_score": similarity_score  # Sorunun transkripte ne kadar benzediği
        })
    
    return evaluation_results

def evaluate_gestures(gesture_data):
    """Jest ve mimik sonuçlarını değerlendirir"""
    scores = []
    
    for gesture in gesture_data:
        eye_openness = gesture["eye_openness"]
        mouth_openness = gesture["mouth_openness"]
        
        if eye_openness > 0.05 and mouth_openness > 0.05:
            score = 1  # Normal
        else:
            score = 0  # Şüpheli veya anormal jest
        
        scores.append(score)
    
    overall_score = sum(scores) / len(scores) if scores else 0
    return overall_score

def evaluate_interview(transcript, gesture_data):
    """Tüm değerlendirmeleri birleştirir"""
    transcript_evaluation = evaluate_transcript_with_questions(transcript)
    gesture_score = evaluate_gestures(gesture_data)
    
    final_score = (sum([result['similarity_score'] for result in transcript_evaluation]) + gesture_score) / (len(transcript_evaluation) + 1)
    
    return {
        "transcript_evaluation": transcript_evaluation,
        "gesture_score": gesture_score,
        "final_score": final_score
    }
