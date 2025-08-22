from langchain_core.documents import Document

# This is where you can add detailed, valid information.
# The more high-quality content you add here, the better the AI's responses will be.

knowledge = [
    {
        "content": "Cognitive Behavioral Therapy (CBT) is a talking therapy that can help you manage your problems by changing the way you think and behave. It's most commonly used to treat anxiety and depression, but can be useful for other mental and physical health problems.",
        "source": "nhs.uk - Overview of CBT"
    },
    {
        "content": "A core principle of CBT is that your thoughts, feelings, physical sensations, and actions are interconnected. Negative thoughts and feelings can trap you in a vicious cycle. CBT aims to help you crack this cycle by breaking down overwhelming problems into smaller parts and showing you how to change these negative patterns.",
        "source": "nhs.uk - How CBT works"
    },
    {
        "content": "Thought Records are a key CBT exercise. You write down a situation, the automatic negative thoughts that arise, the emotions you feel, evidence that supports the negative thought, evidence that contradicts it, and then formulate a more balanced, alternative thought.",
        "source": "beckinstitute.org - Thought Records"
    },
    {
        "content": "Mindfulness is the practice of paying attention to the present moment intentionally and without judgment. This can be done through meditation, but also by simply noticing the sensations of everyday activities like eating or walking.",
        "source": "mindful.org - What is Mindfulness?"
    },
    {
        "content": "A simple mindfulness exercise is the 3-minute breathing space. First, acknowledge what you are thinking and feeling. Second, gently bring your full attention to your breath. Third, expand your awareness to your whole body, noticing any sensations. This can help create a space between you and difficult thoughts.",
        "source": "mindful.org - 3-Minute Breathing Space"
    },
    {
    "content": "Dialectical Behavior Therapy (DBT) is a type of talk therapy based on Cognitive Behavioral Therapy (CBT) but adapted for people who experience emotions very intensely. The term 'dialectical' refers to the synthesis of two opposites: acceptance and change. DBT focuses on helping individuals accept the reality of their lives and behaviors while also teaching them skills to change their lives and unhelpful behaviors.",
    "source": "my.clevelandclinic.org - Dialectical Behavior Therapy (DBT)"
},
{
    "content": "The Biosocial Theory in DBT posits that difficulties in regulating emotions arise from the combination of high emotional sensitivity (a biological factor) and an 'invalidating environment' during childhood. An invalidating environment is one where a person's emotional experiences are consistently dismissed or punished, leading to a failure to learn how to understand, label, and regulate emotions.",
    "source": "asicrecoveryservices.com - DBT Principles: The Complete Guide"
},
{
    "content": "DBT is a structured therapy that focuses on teaching four core skills modules: Mindfulness, Distress Tolerance, Emotion Regulation, and Interpersonal Effectiveness. These skills are designed to replace problematic behaviors with new, more effective ones to help people manage emotions, navigate relationships, and tolerate distress.",
    "source": "dialecticalbehaviortherapy.com - DBT Core Skills"
},
{
    "content": "DBT Mindfulness skills help you focus on and accept the present moment without judgment. This involves three 'What' skills: Observing (just noticing experiences without getting caught in them), Describing (putting words to what you observe), and Participating (throwing yourself completely into the current moment's activity).",
    "source": "yalemedicine.org - Dialectical Behavior Therapy (DBT)"
},
{
    "content": "DBT Mindfulness also includes three 'How' skills, which instruct how to practice the 'What' skills: Non-judgmentally (seeing things as they are, without labeling them as 'good' or 'bad'), One-mindfully (focusing on one thing at a time), and Effectively (doing what works to meet your goals, rather than what feels 'right' or 'fair').",
    "source": "yalemedicine.org - Dialectical Behavior Therapy (DBT)"
},
{
    "content": "Distress Tolerance skills in DBT help you cope with and survive crisis situations without making them worse. These skills are about accepting reality as it is and learning to tolerate intense pain when you cannot immediately change a situation. They provide tools to get through stressful moments with a clear mind.",
    "source": "mcleanhospital.org - What Is Dialectical Behavior Therapy (DBT)?"
},
{
    "content": "A key crisis survival skill in DBT is the TIPP skill, an acronym for changing your body chemistry quickly to reduce extreme emotional arousal. T stands for Temperature (using cold water on your face to trigger the 'dive response' and slow your heart rate). I stands for Intense Exercise (expending stored physical energy). P stands for Paced Breathing (slowing your breathing down). The final P stands for Paired Muscle Relaxation (tensing and then relaxing muscles).",
    "source": "dbt.tools - TIP Skill"
},
{
    "content": "The 'STOP' skill is a distress tolerance technique used to prevent impulsive or emotional actions. It stands for: Stop (freeze, don't react). Take a step back (remove yourself from the situation). Observe (notice what is happening inside and outside of you). Proceed mindfully (act with awareness of your goals).",
    "source": "mcleanhospital.org - What Is Dialectical Behavior Therapy (DBT)?"
},
{
    "content": "The ACCEPTS skill provides ways to distract yourself from painful emotions. It stands for: Activities (do something engaging), Contributing (help someone else), Comparisons (put your situation in perspective), Emotions (create a different feeling), Pushing away (temporarily block the situation from your mind), Thoughts (replace your current thoughts), and Sensations (do something that creates an intense physical sensation, like holding ice).",
    "source": "sunrisertc.com - Distress Tolerance Skills"
},
{
    "content": "The IMPROVE skill helps make a difficult moment better. It stands for: Imagery (imagine a relaxing scene), Meaning (find purpose in the pain), Prayer (connect to a higher power or your own wise mind), Relaxation (take a hot bath or do yoga), One thing in the moment (focus all your attention on the present), Vacation (take a brief break), and Encouragement (be your own cheerleader).",
    "source": "skylandtrail.org - Survive a Crisis Situation with DBT Distress Tolerance Skills"
},
{
    "content": "Self-Soothing with the Five Senses is a distress tolerance skill. To practice it, intentionally engage each of your senses in a comforting way. Vision: Look at a beautiful picture or watch the clouds. Hearing: Listen to calming music or nature sounds. Smell: Light a scented candle or smell fresh laundry. Taste: Slowly savor a piece of chocolate or a warm cup of tea. Touch: Pet an animal or wrap yourself in a soft blanket.",
    "source": "skylandtrail.org - Survive a Crisis Situation with DBT Distress Tolerance Skills"
},
{
    "content": "Radical Acceptance is a reality acceptance skill in DBT. It means completely and totally accepting something from the depths of your soul, with your heart and your mind. It is about acknowledging reality as it is, without judgment or fighting against it, especially when it is painful and cannot be changed. This reduces suffering caused by non-acceptance.",
    "source": "nami.org - Self-Help Techniques for Coping with Mental Illness"
},
{
    "content": "Emotion Regulation in DBT involves skills to understand, be more aware of, and have more control over your emotions. The goal is to manage intense emotional shifts and decrease the distress they cause, helping you to build resilience.",
    "source": "my.clevelandclinic.org - Dialectical Behavior Therapy (DBT)"
},
{
    "content": "A key Emotion Regulation skill is 'Checking the Facts.' This involves describing the prompting event for an emotion, identifying your interpretation of the event, and then examining the actual facts of the situation to see if your emotional response and its intensity are justified by the facts.",
    "source": "dialecticalbehaviortherapy.com - Emotion Regulation"
},
{
    "content": "The 'Opposite-to-Emotion Action' skill involves acting opposite to your emotional urge when the emotion is unjustified or unhelpful. For example, if you feel depressed and have the urge to isolate, the opposite action is to go out and be around people. This can change the emotion itself.",
    "source": "nami.org - Self-Help Techniques for Coping with Mental Illness"
},
{
    "content": "To reduce emotional vulnerability, DBT teaches the 'PLEASE' skills. This involves taking care of your physical health, which directly impacts your emotional state. P L stands for treat Physical iLness, E for balanced Eating, A for Avoid mood-Altering drugs, S for balanced Sleep, and E for get Exercise.",
    "source": "dbt.tools - Emotion Regulation"
},
{
    "content": "Interpersonal Effectiveness skills in DBT help you communicate with others in ways that are assertive, maintain self-respect, and strengthen relationships. These skills help you ask for what you want and say no to what you don't want effectively.",
    "source": "mcleanhospital.org - What Is Dialectical Behavior Therapy (DBT)?"
},
{
    "content": "The 'DEAR MAN' skill is a structured way to make a request or say no. Describe the situation factually. Express your feelings using 'I' statements. Assert your request clearly. Reinforce the positive outcomes of your request being met. Stay Mindful of your goal, ignoring distractions. Appear confident in your posture and tone. Be willing to Negotiate a solution.",
    "source": "dbt.tools - DEAR MAN Skill"
},
{
    "content": "The 'GIVE' skill is used to maintain and improve relationships during conversations. Be Gentle (no attacks or judgments). Act Interested (listen and be present). Validate the other person's feelings and perspective. Use an Easy manner (a light-hearted tone or a smile).",
    "source": "rethinkingresidency.com - DBT Skills for Increasing Interpersonal Effectiveness"
},
{
    "content": "The 'FAST' skill helps you maintain your self-respect in interactions. Be Fair to yourself and the other person. Make no Apologies for making a request or having an opinion. Stick to your values and don't compromise them. Be Truthful and don't act helpless or exaggerate.",
    "source": "rethinkingresidency.com - DBT Skills for Increasing Interpersonal Effectiveness"
},
{
    "content": "Acceptance and Commitment Therapy (ACT) is a form of therapy that helps people learn to accept their difficult thoughts and feelings rather than fighting them. The goal is to create a rich and meaningful life by committing to actions that are guided by your deepest personal values.",
    "source": "psychotherapy.net - Acceptance and Commitment Therapy (ACT)"
},
{
    "content": "A core assumption in ACT is that psychological suffering is often caused by 'experiential avoidance'—the attempt to avoid or get rid of unwanted private experiences like thoughts, feelings, and memories. ACT teaches that these attempts often backfire and lead to more suffering in the long run.",
    "source": "pmc.ncbi.nlm.nih.gov - Acceptance and commitment therapy: an overview of the model, evidence, and applications"
},
{
    "content": "The primary goal of ACT is to increase 'psychological flexibility.' This is the ability to stay in contact with the present moment and, depending on the situation, either persist with or change your behavior in the service of your chosen values. It is cultivated through six core processes.",
    "source": "pmc.ncbi.nlm.nih.gov - Acceptance and commitment therapy: an overview of the model, evidence, and applications"
},
{
    "content": "Cognitive Defusion involves creating distance from your thoughts, allowing you to see them as just 'bits of language' passing through your mind, rather than as objective truths or commands you must obey. This reduces their power over your actions.",
    "source": "contextualconsulting.co.uk - ACT basics - The six core processes"
},
{
    "content": "A simple Cognitive Defusion exercise is to preface a difficult thought with the phrase, 'I'm having the thought that...' For example, instead of 'I am a failure,' you would practice saying, 'I'm having the thought that I am a failure.' This small linguistic shift helps create separation between you and the thought.",
    "source": "simplepractice.com - Cognitive Defusion Techniques"
},
{
    "content": "Another defusion technique is to visualize your thoughts as leaves floating down a stream or clouds passing in the sky. You place each thought on a leaf or cloud and simply watch it come into view and then float away, without getting attached to it or trying to change it.",
    "source": "firstpsychology.co.uk - ACT defusion techniques"
},
{
    "content": "Acceptance, also called 'expansion,' is the practice of making room for unpleasant feelings, sensations, and urges, instead of trying to suppress or push them away. By opening up and allowing them to be there, they tend to bother you less and pass more quickly.",
    "source": "aipc.net.au - Six Principles of Acceptance and Commitment Therapy"
},
{
    "content": "To practice Acceptance, you can try a body scan meditation. When you notice a difficult sensation, instead of fighting it, you observe it with curiosity. Notice its location, size, shape, and temperature, and breathe into the sensation, creating space for it in your body.",
    "source": "positivepsychology.com - ACT Acceptance and Commitment Therapy"
},
{
    "content": "Contact with the Present Moment means bringing your full awareness to the here-and-now with openness and receptiveness, rather than dwelling on the past or worrying about the future. The power to act exists only in the present.",
    "source": "aipc.net.au - Six Principles of Acceptance and Commitment Therapy"
},
{
    "content": "A simple exercise for contacting the present moment is the 'Five Senses' technique. Pause and intentionally notice: 5 things you can see, 4 things you can physically feel, 3 things you can hear, 2 things you can smell, and 1 thing you can taste. This anchors you in your current sensory experience.",
    "source": "positivepsychology.com - ACT Worksheets"
},
{
    "content": "The Observing Self, or 'Self-as-Context,' is the part of you that is aware of your experiences but is not the experiences themselves. It is a stable, safe perspective from which you can notice your thoughts and feelings without being defined by them, like the sky that holds the ever-changing weather.",
    "source": "providence.org - ACT and The Observing Self"
},
{
    "content": "To connect with your Observing Self, practice noticing the distinction between your thoughts and the 'you' who is noticing them. An exercise is to say to yourself: 'There are my thoughts, and here I am, noticing them. There are my feelings, and here I am, noticing them.' This reinforces that you are the container, not the content.",
    "source": "nurturingmindscounseling.com - Understanding and Embracing the Observing Self"
},
{
    "content": "Values are your heart's deepest desires for how you want to behave as a human being. They are not goals to be achieved, but chosen life directions, like heading west. Values provide motivation and guidance for your actions.",
    "source": "thehappinesstrap.com - Clarifying Your Values"
},
{
    "content": "A common values clarification exercise is the 'Tombstone Exercise.' Imagine your own funeral and what you would want your loved ones to say about you. What personal qualities and ways of living would you want to be remembered for? This can help you identify what truly matters to you.",
    "source": "cerebral.com - ACT Skills: Clarifying Values"
},
{
    "content": "Committed Action means taking effective action guided by your values. It involves setting goals that are in line with your values and taking steps to achieve them, even if it brings up difficult thoughts and feelings.",
    "source": "contextualconsulting.co.uk - ACT basics - The six core processes"
},
{
    "content": "To practice Committed Action, first clarify a value in a specific life domain (e.g., 'being a supportive friend'). Then, set a SMART goal related to that value (Specific, Measurable, Achievable, Relevant, Time-bound), such as 'I will call my friend who is going through a hard time this Tuesday evening to check in.'",
    "source": "ucsbpositivepsych.org - PERMA Model"
},
{
    "content": "Psychodynamic therapy is an approach focused on helping people gain insight into the roots of their emotional suffering. It posits that much of our behavior is influenced by unconscious thoughts, feelings, and memories that are outside of our immediate awareness.",
    "source": "verywellmind.com - Types of Therapy: An A to Z List of Your Options"
},
{
    "content": "A core principle of psychodynamic thought is that our early childhood experiences, particularly our relationships with caregivers, have a profound and lasting impact on our personality and how we form relationships in adulthood. These early patterns are often unconsciously repeated in our current lives.",
    "source": "simplypsychology.org - Psychodynamic Approach"
},
{
    "content": "Defense Mechanisms are unconscious psychological strategies we use to cope with anxiety and protect ourselves from distressing thoughts or feelings. Common examples include denial (refusing to accept reality), repression (pushing unwanted thoughts into the unconscious), and displacement (redirecting feelings onto a less threatening target).",
    "source": "icsw.edu - What is Psychodynamic Therapy?"
},
{
    "content": "Journaling Prompt: Reflect on a recent strong emotional reaction you had. Can you identify any defense mechanisms you might have used? For example, did you use humor to deflect from a serious topic (intellectualization), or blame someone else for your feelings (projection)? Recognizing these patterns is the first step to understanding them.",
    "source": "therapygroupdc.com - What is Psychodynamic Therapy?"
},
{
    "content": "Transference is a psychodynamic concept where we unconsciously redirect feelings and attitudes from a person in our past (like a parent) onto someone in the present. For example, you might feel an unexplained irritation toward a boss who is not objectively doing anything wrong, because they remind you of a critical parent.",
    "source": "ncbi.nlm.nih.gov - Psychodynamic Therapy"
},
{
    "content": "Journaling Prompt: Consider your key relationships. Do you notice any recurring themes or patterns in how you interact with people? For example, do you often find yourself in a caretaking role, or do you tend to seek approval? These patterns often have roots in our earliest relationships and understanding them can lead to healthier interactions.",
    "source": "therapygroupdc.com - What is Psychodynamic Therapy?"
},
{
    "content": "Eye Movement Desensitization and Reprocessing (EMDR) is a psychotherapy primarily used to help individuals process distressing memories, particularly those related to trauma and PTSD. The therapy involves recalling the traumatic event while engaging in bilateral stimulation, such as guided eye movements, which is thought to facilitate the brain's natural healing and information processing abilities.",
    "source": "spearheadhealth.com - Different Therapeutic Modalities"
},
{
    "content": "Art Therapy utilizes creative expression, such as painting, drawing, or collage, as a way to explore and communicate emotions. It is especially beneficial for those who find it difficult to verbalize their feelings and can be helpful for a range of issues including anxiety and PTSD.",
    "source": "verywellmind.com - Types of Therapy: An A to Z List of Your Options"
},
{
    "content": "Motivational Interviewing (MI) is a collaborative counseling style for strengthening a person's own motivation and commitment to change. It is a person-centered approach that helps individuals explore and resolve ambivalence about changing behaviors, such as in cases of substance abuse or adopting healthier habits.",
    "source": "spearheadhealth.com - Different Therapeutic Modalities"
},
{
    "content": "Family Therapy recognizes the impact of family dynamics on an individual's mental health. It involves working with family members to improve communication, resolve conflicts, and create a more supportive home environment. It is particularly effective for addressing issues like substance abuse, eating disorders, and relationship difficulties.",
    "source": "spearheadhealth.com - Different Therapeutic Modalities"
},
{
    "content": "Interpersonal Psychotherapy (IPT) is a time-limited therapy that focuses on improving interpersonal relationships and social functioning to resolve psychological problems. It is particularly helpful for those dealing with depression related to grief, major life transitions, or conflicts in relationships.",
    "source": "therapygroupdc.com - CBT vs Other Therapy Approaches"
},
{
    "content": "The 5-4-3-2-1 Grounding Technique is a simple exercise to use during periods of anxiety or panic. Pause and notice: FIVE things you can see around you. FOUR things you can touch. THREE things you can hear. TWO things you can smell. ONE thing you can taste. This exercise brings you back to the present by engaging all your senses.",
    "source": "urmc.rochester.edu - 5-4-3-2-1 Coping Technique for Anxiety"
},
{
    "content": "Physical grounding techniques use your body to anchor you. Try pressing your feet firmly into the floor, noticing the sensation of the ground beneath you. You can also hold a piece of ice in your hand, focusing on the intense cold, or run your hands under water, paying attention to the temperature and pressure.",
    "source": "healthline.com - Grounding Techniques"
},
{
    "content": "Mental grounding techniques use cognitive tasks to distract from anxiety. Try a category game: pick a category like 'animals' or 'fruits' and name as many items as you can. Another technique is to count backward from 100 by 7s. These tasks require focus and pull your mind away from anxious thoughts.",
    "source": "hr.jhu.edu - Grounding Techniques to Help Control Anxiety"
},
{
    "content": "Deep Belly Breathing is a fundamental relaxation technique. Sit or lie down comfortably. Place one hand on your chest and the other on your belly. Breathe in slowly through your nose for a count of four, feeling your belly rise. Hold for a moment, then exhale slowly through your mouth for a count of six. The longer exhale signals your nervous system to calm down.",
    "source": "webmd.com - Ways to Manage Stress"
},
{
    "content": "Box Breathing is a simple technique to regulate your breath and calm your nervous system. Inhale slowly for a count of 4. Hold your breath for a count of 4. Exhale slowly for a count of 4. Hold your breath again for a count of 4. Repeat the cycle several times.",
    "source": "calmerry.com - Simple Grounding Techniques for Anxiety"
},
{
    "content": "Progressive Muscle Relaxation (PMR) is a deep relaxation technique that involves systematically tensing and then relaxing different muscle groups. This process helps you become more aware of physical tension and learn to release it. It can significantly reduce feelings of anxiety and stress.",
    "source": "unr.edu - Stress and Anxiety Management Skills"
},
{
    "content": "To practice Progressive Muscle Relaxation, start with your feet. Inhale and tense the muscles in your feet and toes for 5-10 seconds. Then, exhale and completely release the tension, noticing the feeling of relaxation. Work your way up your body, tensing and relaxing muscle groups in your legs, abdomen, arms, and face.",
    "source": "mayoclinic.org - Progressive muscle relaxation: A simple technique for reducing stress and anxiety"
},
{
    "content": "Mindful Breathing is the practice of focusing your attention on your breath. Find a comfortable position. Notice the sensation of the air entering your nostrils, filling your lungs, and then leaving your body. When your mind wanders, gently and without judgment, guide your attention back to your breath. Your breath is an anchor to the present moment.",
    "source": "va.gov - A Mindful Breathing Script"
},
{
    "content": "A key strategy for depression is Behavioral Activation. This involves scheduling and participating in activities that are either pleasant or provide a sense of accomplishment, even if you don't feel motivated to do them. Start small, like taking a 10-minute walk or listening to one song. Action can create motivation.",
    "source": "intermountainhealthcare.org - 7 Ways to Overcome Depression Without Medication"
},
{
    "content": "Establish a daily routine. When you feel depressed, routines can fall apart. Try to get up at the same time each day, eat meals at regular times, and maintain basic hygiene. A consistent schedule provides structure and predictability, which can be stabilizing when your mood is low.",
    "source": "nhs.uk - Cope with depression"
},
{
    "content": "Stay connected with others. Depression often leads to an urge to withdraw and isolate, but social connection is a powerful mood booster. Make an effort to keep in touch with friends and family, even if it's just a short text or phone call. You don't have to talk about your depression; just connecting can help.",
    "source": "nhs.uk - Cope with depression"
},
{
    "content": "Set realistic goals. Depression can make tasks feel overwhelming. Break down larger goals into very small, concrete steps. For example, instead of 'clean the house,' a smaller goal could be 'put one dish in the dishwasher.' Regaining a sense of accomplishment, no matter how small, helps counter feelings of hopelessness.",
    "source": "mayoclinic.org - Depression: Diagnosis and treatment"
},
{
    "content": "Challenge negative thoughts by paying attention to warning signs. Work with a therapist or use a journal to learn what triggers your depressive symptoms. When you notice negative beliefs, try to identify evidence that contradicts them and formulate a more balanced, positive alternative.",
    "source": "mayoclinic.org - Depression: Diagnosis and treatment"
},
{
    "content": "Practice self-compassion. When you're struggling, respond to yourself with the same kindness and understanding you would offer a friend. Self-compassion reduces the negative feelings caused by self-criticism and helps you navigate difficult emotions without judgment.",
    "source": "unr.edu - Stress and Anxiety Management Skills"
},
{
    "content": "Engage in peer support. Connecting with others who have similar experiences can be incredibly validating. Peer support can be found in formal groups or online communities. Peers can serve as proof that recovery is possible and offer practical knowledge for daily management of your condition.",
    "source": "depressioncenter.org - Self-Help"
},
{
    "content": "Identify your stress triggers. Keep a journal for a week or two to identify the situations, people, or thoughts that cause you the most stress. Once you know your triggers, you can work on either avoiding them or changing your reaction to them.",
    "source": "adaa.org - Tips to Manage Anxiety and Stress"
},
{
    "content": "Practice the '4 A's' of stress management: Avoid, Alter, Adapt, and Accept. Avoid unnecessary stress (e.g., say no). Alter the situation (e.g., express your feelings). Adapt to the stressor (e.g., reframe the problem). Accept the things you can't change.",
    "source": "mayoclinic.org - Stress management"
},
{
    "content": "Improve your time management. Feeling overwhelmed by a long to-do list is a major source of stress. Prioritize your tasks using a system like the Eisenhower Matrix (urgent/important) and break large projects into smaller, more manageable steps. Taking control of your schedule is empowering.",
    "source": "grad.uc.edu - Six Strategies for Effective Stress Management"
},
{
    "content": "Make time for relaxation and hobbies. Intentionally schedule time for activities you enjoy, whether it's reading, gardening, listening to music, or a creative project. This 'me time' is not a luxury; it is essential for recharging and preventing burnout.",
    "source": "nhs.uk - Tips to reduce stress"
},
{
    "content": "Assert yourself and set boundaries. Instead of being passive or aggressive, learn to communicate your feelings, opinions, and beliefs in an assertive, respectful way. This includes learning to say 'no' to requests that would add excessive stress to your life.",
    "source": "webmd.com - Ways to Manage Stress"
},
{
    "content": "Use humor and laughter. A good laugh can fire up and then cool down your stress response. It increases your intake of oxygen-rich air, stimulates circulation, and can soothe tension. Actively seek out humor by watching a comedy, reading jokes, or spending time with funny friends.",
    "source": "mayoclinic.org - Stress relievers: Tips to tame stress"
},
{
    "content": "Build a strong social support network. Connecting with friends and family can offer distraction, provide support, and help you weather life's ups and downs. Don't isolate yourself when you're stressed; reach out and share what you're going through.",
    "source": "mayoclinic.org - Stress relievers: Tips to tame stress"
},
{
    "content": "Sleep hygiene refers to healthy habits and practices that are conducive to sleeping well on a regular basis. Good sleep hygiene is crucial for mental health, as sleep disruption is linked to increased stress, mood disorders, and emotional distress.",
    "source": "verywellmind.com - What Is Sleep Hygiene?"
},
{
    "content": "Maintain a consistent sleep schedule. Go to bed and wake up at approximately the same time every day, including on weekends. This helps regulate your body's internal clock, or circadian rhythm, leading to better quality sleep.",
    "source": "sleepfoundation.org - Mental Health and Sleep"
},
{
    "content": "Create a relaxing pre-sleep routine. In the hour before bed, engage in calming activities like reading a physical book, taking a warm bath, listening to soothing music, or practicing gentle stretching. This helps signal to your body and mind that it's time to wind down.",
    "source": "verywellmind.com - What is Sleep Hygiene?"
},
{
    "content": "Optimize your sleep environment. Your bedroom should be cool, dark, and quiet. Use blackout curtains, an eye mask, or earplugs if necessary. A comfortable and supportive mattress and pillows are also essential.",
    "source": "sleepfoundation.org - Mental Health and Sleep"
},
{
    "content": "Turn off all electronic devices at least 60 minutes before bed. The blue light emitted by phones, tablets, and computers can suppress the production of melatonin, the hormone that controls your sleep-wake cycle, making it harder to fall asleep.",
    "source": "verywellmind.com - What is Sleep Hygiene?"
},
{
    "content": "Avoid stimulants like caffeine and nicotine, especially in the afternoon and evening. Caffeine can stay in your system for many hours and interfere with your ability to fall asleep. It's best to avoid it for at least 4-6 hours before bedtime.",
    "source": "cci.health.wa.gov.au - Sleep Hygiene"
},
{
    "content": "Limit alcohol before bed. While alcohol may make you feel sleepy initially, it disrupts the quality of your sleep later in the night, leading to more frequent awakenings and less restorative rest.",
    "source": "sleepfoundation.org - Mental Health and Sleep"
},
{
    "content": "Get regular exercise, but time it right. Daily physical activity can promote better sleep. However, try to avoid strenuous exercise within a few hours of bedtime, as it can be too stimulating. Gentle activities like yoga or stretching are fine in the evening.",
    "source": "cci.health.wa.gov.au - Sleep Hygiene"
},
{
    "content": "If you can't fall asleep within about 20 minutes, get out of bed. Go to another room and do something quiet and relaxing in dim light until you feel sleepy. Tossing and turning in bed can create a frustrating association between your bed and wakefulness.",
    "source": "cci.health.wa.gov.au - Sleep Hygiene"
},
{
    "content": "The food you eat has a direct impact on your mental health. A healthy diet rich in fruits, vegetables, whole grains, and lean proteins can reduce inflammation and provide essential nutrients for brain function, helping to lessen symptoms of depression and anxiety.",
    "source": "aetna.com - What you eat affects your mental health"
},
{
    "content": "The Mediterranean diet is one of the most well-researched eating patterns for mental health. It emphasizes fruits, vegetables, nuts, legumes, whole grains, fish, and olive oil, while limiting red meat and processed foods. Studies show it can significantly improve symptoms of depression.",
    "source": "psychiatry.org - Mental Health Through Better Nutrition"
},
{
    "content": "Eat foods rich in Omega-3 fatty acids to support brain health. These healthy fats, found in fatty fish like salmon and sardines, as well as in walnuts and flaxseeds, have anti-inflammatory properties and are crucial for brain cell function. Low intake is linked to higher rates of depression.",
    "source": "webmd.com - Depression and Diet"
},
{
    "content": "Choose complex carbohydrates over simple ones. Complex carbs from sources like whole grains (oatmeal, quinoa), beans, and vegetables release glucose slowly, which helps stabilize blood sugar and mood. Simple carbs from sugary foods and white flour can cause energy spikes and crashes that worsen anxiety.",
    "source": "mayoclinic.org - Coping with anxiety"
},
{
    "content": "Ensure adequate intake of B vitamins, especially folate and B12. Deficiencies in these vitamins are linked to depression. Good sources of folate include leafy greens (spinach, kale), lentils, and beans. B12 is found in lean meats, fish, and dairy products.",
    "source": "webmd.com - Depression and Diet"
},
{
    "content": "Support your gut microbiome with probiotics and prebiotics. Probiotics are beneficial bacteria found in fermented foods like yogurt with live cultures, kefir, and sauerkraut. Prebiotics are fibers that feed these bacteria, found in foods like garlic, onions, bananas, and oats. A healthy gut is linked to better mood regulation.",
    "source": "intermountainhealthcare.org - 7 ways to boost your mood with food"
},
{
    "content": "Limit or avoid ultra-processed foods, added sugars, and sugary drinks. These foods offer little nutritional value, promote inflammation, and can lead to mood swings and energy crashes. Studies link diets high in processed foods to a greater risk of developing depression and anxiety.",
    "source": "sutterhealth.org - Eating Well for Mental Health"
},
{
    "content": "Stay hydrated by drinking plenty of water. Even mild dehydration can negatively affect your mood, increase irritability, and impair concentration. Water is essential for making the neurotransmitters and hormones that regulate brain processes.",
    "source": "healthdirect.gov.au - Food, drink and mental health"
},
{
    "content": "Magnesium is a vital mineral for the food-mood connection, and a lack of it can contribute to anxiety and depression symptoms. Load up on natural sources like dark leafy greens (spinach), almonds, cashews, bananas, and beans.",
    "source": "aetna.com - What you eat affects your mental health"
},
{
    "content": "Regular physical activity is a powerful tool for mental wellness. It can reduce symptoms of depression and anxiety, boost mood, improve concentration, and enhance self-esteem. Any amount of activity is better than none, and finding an activity you enjoy is key to consistency.",
    "source": "betterhealth.vic.gov.au - Exercise and mental health"
},
{
    "content": "Exercise boosts your mood by releasing feel-good brain chemicals called endorphins. It also influences other chemicals like serotonin and stress hormones. This can lead to a natural energy boost and a more positive outlook on life.",
    "source": "mayoclinic.org - Depression and exercise: Easing symptoms"
},
{
    "content": "Aerobic exercises like brisk walking, jogging, swimming, or cycling are particularly effective at reducing anxiety and depression. Aim for at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity activity per week.",
    "source": "mayoclinic.org - Exercise and stress: Get moving to manage stress"
},
{
    "content": "Strength training, such as lifting weights or using resistance bands, not only builds physical strength but also improves mood and self-esteem. It can be an effective way to release tension and feel a sense of accomplishment.",
    "source": "timesofindia.indiatimes.com - Exercise for chronic pain"
},
{
    "content": "Mind-body practices like yoga and tai chi combine physical postures, breathing exercises, and meditation. They are excellent for reducing stress, lowering blood pressure, and calming the nervous system, which helps to ease anxiety and improve mood.",
    "source": "verywellmind.com - Mental Health Benefits of Exercise"
},
{
    "content": "Exercising outdoors in nature can provide an extra mental health boost. Research shows that being in green spaces can make us feel happier, reduce depression and anxiety, and increase feelings of vitality.",
    "source": "mentalhealth.org.uk - Physical activity and mental health"
},
{
    "content": "You don't need a structured program to benefit. Activities like gardening, washing your car, dancing, or taking the stairs instead of the elevator all count. The goal is to reduce sedentary time and incorporate more movement into your daily life.",
    "source": "mayoclinic.org - Depression and exercise: Easing symptoms"
},
{
    "content": "To stay motivated, set reasonable goals. Instead of aiming for a one-hour workout every day, start with a 15-minute walk. Don't think of exercise as a chore, but as a tool to help you feel better. Celebrate small achievements to build confidence.",
    "source": "mayoclinic.org - Depression and exercise: Easing symptoms"
},
{
    "content": "The PERMA model is a framework for well-being with five core elements: Positive Emotion, Engagement, Relationships, Meaning, and Accomplishment. Focusing on these five areas can help you build a more fulfilling and satisfying life.",
    "source": "ppc.sas.upenn.edu - PERMA Theory of Well-Being"
},
{
    "content": "P is for Positive Emotion. This is about more than just happiness; it includes emotions like joy, gratitude, hope, and love. You can cultivate positive emotions by savoring good moments, reflecting on things you're grateful for, and maintaining an optimistic outlook.",
    "source": "positivepsychology.com - The PERMA Model"
},
{
    "content": "E is for Engagement. This refers to being fully absorbed in an activity, often called a state of 'flow.' You can increase engagement by identifying your top character strengths and finding new ways to use them in activities you enjoy, where you lose track of time.",
    "source": "liveonpurpose.ca - Top 10 Exercises for Well-Being"
},
{
    "content": "R is for Relationships. Humans are social beings, and strong, supportive relationships are fundamental to well-being. Nurture your connections by spending quality time with loved ones and practicing active-constructive responding—reacting enthusiastically to their good news.",
    "source": "viacharacter.org - Your Relationships Are Pathways to Thriving"
},
{
    "content": "M is for Meaning. This is about belonging to and serving something you believe is bigger than yourself. You can build meaning by getting involved in a cause you care about, using your passions to help others, or connecting with your spirituality.",
    "source": "planetpositivechange.com - PERMA M is for Meaning"
},
{
    "content": "A is for Accomplishment. This involves pursuing and achieving goals, which builds self-esteem and a sense of mastery. Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound) that align with your values and remember to celebrate your successes, no matter how small.",
    "source": "planetpositivechange.com - PERMA A is for Accomplishment"
},
{
    "content": "A Gratitude Journal is a simple and effective practice. Each day or once a week, write down three to five things you are grateful for. Be specific: instead of just 'my family,' write 'the way my partner made me laugh today.' This detail helps evoke a genuine feeling of gratitude.",
    "source": "calm.com - Gratitude Exercises"
},
{
    "content": "The 'Three Good Things' exercise, developed by Dr. Martin Seligman, involves writing down three things that went well each day and reflecting on why they happened. This practice has been shown to increase happiness and decrease depressive symptoms, with effects lasting for months.",
    "source": "pcom.edu - Examples of Positive Psychology"
},
{
    "content": "Write a Gratitude Letter to someone who has made a positive difference in your life but whom you have never properly thanked. Write in detail about what they did and how it affected you. If possible, deliver the letter and read it to them in person for the maximum positive impact on both of you.",
    "source": "cdc.gov - Gratitude Works"
},
{
    "content": "Take a Gratitude Walk. Go for a walk with the specific intention of noticing things in your environment that you can be grateful for. Use all your senses: the warmth of the sun, the sound of birds, the color of the flowers, the smell of fresh air. This is a form of moving meditation.",
    "source": "calm.com - Gratitude Exercises"
},
{
    "content": "Create a Gratitude Jar. Write down things you are grateful for on small slips of paper and place them in a jar. Whenever you need a mood boost, you can pull a few slips out and remind yourself of the good things in your life.",
    "source": "positivepsychology.com - Gratitude Exercises"
},
{
    "content": "Character Strengths are positive personality traits that impact how you think, feel, and behave. The VIA Classification identifies 24 universal strengths that everyone possesses in different degrees. Knowing your top strengths can help you live a more authentic and fulfilling life.",
    "source": "viacharacter.org - Character Strengths"
},
{
    "content": "To discover your unique character strengths profile, you can take the free, scientifically validated VIA Survey online. The results will rank all 24 strengths, highlighting your 'signature strengths'—those that are most core to who you are.",
    "source": "viacharacter.org - Character Strengths"
},
{
    "content": "Your 'signature strengths' are typically your top 5-7 strengths from the VIA Survey. These are the strengths that feel natural, easy, and energizing for you to use. They represent you at your best and are essential to your personal identity.",
    "source": "viacharacter.org - VIA Total 24 Report Interpretation Guide"
},
{
    "content": "A powerful exercise is to 'Use a Signature Strength in a New Way.' Pick one of your top strengths and brainstorm a new way to apply it each day for a week. For example, if 'Curiosity' is a top strength, you could try a new type of food, read about a topic you know nothing about, or ask a colleague about their work with genuine interest.",
    "source": "pcom.edu - Examples of Positive Psychology"
},
{
    "content": "Focusing on your strengths is more effective for building well-being than trying to fix your weaknesses. While it's important to manage lesser strengths, actively using your signature strengths is associated with significant improvements in mood and life satisfaction.",
    "source": "viacharacter.org - Your Relationships Are Pathways to Thriving"
},
{
    "content": "Resilience is the process of adapting well in the face of adversity. A key factor in building resilience is making and maintaining connections. Having a strong network of supportive family and friends provides social support and acts as a protective buffer during stressful times.",
    "source": "apa.org - 10 tips for building resilience"
},
{
    "content": "Nurture a positive self-view by believing in your abilities. Remind yourself of past challenges you have successfully handled. This helps build confidence in your ability to cope with future hardships. When you hear negative self-talk, practice replacing it with positive statements like, 'I can handle this.'",
    "source": "verywellmind.com - Ways to Become More Resilient"
},
{
    "content": "Find a sense of purpose. Connecting your daily actions to a larger meaning or value helps you find motivation to persevere through difficult times. This could involve serving your community, dedicating yourself to a cause, or cultivating your spirituality.",
    "source": "verywellmind.com - Ways to Become More Resilient"
},
{
    "content": "Maintain a hopeful and optimistic outlook. While you can't change difficult events, you can change how you interpret and respond to them. Try to see beyond the current situation and remember that setbacks are temporary. An optimistic outlook empowers you to expect that good things will happen.",
    "source": "apa.org - 10 tips for building resilience"
},
{
    "content": "Embrace change and cultivate flexibility. Resilient people are often more adaptable. They view challenges not as insurmountable obstacles, but as opportunities to learn and grow. Practice looking at difficult situations from different perspectives to find creative solutions.",
    "source": "verywellmind.com - Ways to Become More Resilient"
},
{
    "content": "Practice self-care. Looking after your physical health is fundamental to resilience. Prioritize getting enough sleep, eating a nutritious diet, and engaging in regular physical activity. These habits keep your mind and body strong enough to deal with stressful situations.",
    "source": "mind.org.uk - Managing stress and building resilience"
},
{
    "content": "Move toward your goals. Develop realistic goals and regularly do something that moves you toward them, even if it feels like a small step. This helps you focus on the future and builds a sense of agency and control over your life, rather than feeling helpless.",
    "source": "apa.org - 10 tips for building resilience"
}

    
]

# Transform the list of dictionaries into a list of Document objects
documents = [Document(page_content=item["content"], metadata={"source": item["source"]}) for item in knowledge]