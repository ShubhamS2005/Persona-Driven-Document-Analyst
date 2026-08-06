from modules.persona.persona_detector import PersonaDetector



detector=PersonaDetector()



queries=[

    "What are the historical sites in Carcassonne?",

    "What places should I visit in South France?",

    "Explain the medieval architecture of Carcassonne"

]



for q in queries:


    result=detector.detect(q)


    print("\nQUERY:")
    print(q)


    print(
        "PERSONA:",
        result["persona"]
    )


    print(
        "CONFIDENCE:",
        result["confidence"]
    )