"""
SkinCare AI - Disease-Specific Medical Education & Recommendations
Covers all 23 dataset categories with detailed causes, prevention, daily care,
treatment options, dietary notes, and urgency flags.

DISCLAIMER: Educational information only, not a clinical diagnosis or prescription.
"""

SKIN_RECOMMENDATIONS = {
    "Acne and Rosacea Photos": {
        "description": "Acne vulgaris is a chronic inflammatory disorder of the pilosebaceous units, whereas rosacea is a vascular/inflammatory facial condition causing persistent erythema and telangiectasia.",
        "causes": [
            "Excess sebum (oil) production driven by hormonal fluctuations (androgens).",
            "Clogged pores from dead skin cells (hyperkeratinization) and Cutibacterium acnes bacteria proliferation.",
            "Rosacea triggers: Dysregulated neurovascular control, Demodex mites, heat, ultraviolet radiation, and spicy foods.",
            "Genetics, cosmetic irritants, and friction from tight masks or clothing."
        ],
        "prevention": [
            "Cleanse gently twice daily with a non-stripping, pH-balanced cleanser; avoid harsh scrubs.",
            "Select only non-comedogenic and oil-free moisturizers, sunscreens, and cosmetics.",
            "Never squeeze, pop, or pick pimples to prevent secondary scarring and deep cysts.",
            "For rosacea, identify and avoid personal flare triggers (extreme hot/cold temperatures, alcohol, spicy foods).",
            "Wear broad-spectrum daily SPF 30+ mineral sunscreen (zinc oxide or titanium dioxide are gentle for rosacea)."
        ],
        "care": [
            "Wash your face gently twice daily with lukewarm water and a mild non-foaming or foaming cleanser.",
            "Use lightweight, oil-free hydrators containing hyaluronic acid, ceramides, or niacinamide.",
            "Avoid hot water, washcloth scrubbing, and alcohol-based toners or astringents.",
            "Change pillowcases frequently and disinfect phone screens regularly."
        ],
        "treatment": (
            "Acne is typically managed with topical retinoids, benzoyl peroxide, azelaic acid, salicylic acid, "
            "and in moderate-to-severe cases, oral antibiotics or isotretinoin under dermatological supervision. "
            "Rosacea responds to topical ivermectin, metronidazole, azelaic acid, or oral doxycycline. "
            "Consult a dermatologist for a tailored prescription regimen."
        ),
        "foods": (
            "Evidence shows high-glycemic-load diets (sugary beverages, refined carbs) and skim dairy may exacerbate acne "
            "in some individuals. For rosacea, hot beverages, spicy foods, and alcohol often trigger immediate facial flushing. "
            "Maintain a balanced, nutrient-dense diet rich in omega-3 fatty acids and antioxidants."
        ),
        "urgency": (
            "Consult a clinician promptly for deep painful cystic nodules, spreading inflammation, risk of permanent scarring, "
            "or ocular symptoms (red, gritty, painful eyes, which can indicate ocular rosacea)."
        )
    },

    "Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions": {
        "description": "Actinic keratosis (AK) is a rough precancerous sun-damaged lesion that can progress to squamous cell carcinoma. Basal cell carcinoma (BCC) is the most common form of skin cancer, arising from the basal layer of the epidermis.",
        "causes": [
            "Cumulative lifetime exposure to ultraviolet (UV) radiation from sunlight or artificial tanning beds.",
            "DNA mutations (e.g., TP53 gene damage) caused by chronic UV radiation in keratinocytes.",
            "Fair skin, light hair, light eyes, tendency to burn easily, and older age.",
            "Immunosuppression from organ transplantation or immunosuppressive medications."
        ],
        "prevention": [
            "Strict daily broad-spectrum sun protection with SPF 50+ sunscreen, reapplying every 2 hours outdoors.",
            "Wear UV-protective clothing, wide-brimmed hats, and UV-blocking sunglasses.",
            "Avoid peak sun hours (10:00 AM to 4:00 PM) and seek shade whenever possible.",
            "Completely avoid indoor tanning beds and sunlamps.",
            "Perform monthly full-body skin self-checks using a mirror to detect any new, changing, or non-healing lesions.",
            "Attend annual professional total-body skin exams with a board-certified dermatologist."
        ],
        "care": [
            "Protect the lesion from trauma, scratches, and friction from clothing.",
            "Do not attempt to scrape, peel, freeze, burn, or treat the lesion with unproven home remedies.",
            "Photograph the spot with a measuring tape beside it to track any changes in size, border, or elevation."
        ],
        "treatment": (
            "Precancerous AKs are treated with cryotherapy (liquid nitrogen), topical 5-fluorouracil (5-FU), imiquimod, "
            "or photodynamic therapy (PDT). Basal cell carcinomas are treated by surgical excision, Mohs micrographic surgery, "
            "curettage and electrodesiccation, or topical agents for superficial subtypes. Histological evaluation is mandatory."
        ),
        "foods": (
            "No specific diet replaces oncological evaluation. A diet rich in Mediterranean-style foods, antioxidants, "
            "and nicotinamide (vitamin B3, under medical guidance) may help support skin repair mechanisms."
        ),
        "urgency": (
            "Urgent: Seek dermatological consultation for any pearly nodule with visible telangiectasia, firm red nodule, "
            "sore that does not heal within 3-4 weeks, or recurring crusting/bleeding growth."
        )
    },

    "Atopic Dermatitis Photos": {
        "description": "Atopic dermatitis is a chronic, relapsing, highly pruritic inflammatory skin disorder linked to genetic skin barrier dysfunction (such as filaggrin mutations) and immune system overactivity.",
        "causes": [
            "Genetic mutations in the filaggrin gene (FLG), compromising the epidermal stratum corneum barrier.",
            "Immune system dysregulation with predominant Type 2 (Th2) inflammatory cytokine pathways (IL-4, IL-13).",
            "Environmental allergens: dust mites, pollen, pet dander, wool, and harsh chemical irritants.",
            "Climatic triggers: cold, dry weather, low humidity, and sudden temperature shifts.",
            "Microbiome dysbiosis with overgrowth of Staphylococcus aureus on eczematous lesions."
        ],
        "prevention": [
            "Maintain skin barrier integrity through the 'soak and seal' method: apply thick ceramide cream within 3 minutes of bathing.",
            "Use only unscented, hypoallergenic detergents and fragrance-free hygiene products.",
            "Keep fingernails short and smooth to minimize epidermal trauma from scratching, especially at night.",
            "Maintain moderate indoor humidity (40-50%) using humidifiers during dry winter months.",
            "Wear soft, breathable 100% cotton garments and avoid wool or rough synthetic textiles."
        ],
        "care": [
            "Take short (5-10 minute) lukewarm baths or showers once daily; avoid hot water.",
            "Liberally apply fragrance-free ointments or thick creams (petrolatum, ceramides) 2-3 times daily.",
            "Use wet wrap therapy during acute flares if recommended by a healthcare provider.",
            "Apply cold compresses or calamine lotion to soothe intense itching without skin breakdown."
        ],
        "treatment": (
            "Topical corticosteroids remain first-line for flare control. Topical calcineurin inhibitors (tacrolimus, pimecrolimus) "
            "and PDE4 inhibitors (crisaborole) provide steroid-sparing maintenance. Moderate-to-severe cases may require biologics "
            "(e.g., dupilumab, tralokinumab) or JAK inhibitors under medical supervision."
        ),
        "foods": (
            "True food allergies trigger eczema flares primarily in young children (eggs, milk, peanuts). In adults, routine "
            "unsupervised food elimination can lead to nutritional deficiencies without curing eczema. Only eliminate foods with confirmed allergist testing."
        ),
        "urgency": (
            "Seek urgent medical evaluation for yellow honey-colored crusting, pustules, painful weeping skin, rapid spread "
            "accompanied by fever, or widespread small painful blisters (which can indicate eczema herpeticum, an emergency)."
        )
    },

    "Bullous Disease Photos": {
        "description": "Bullous diseases encompass autoimmune blistering disorders (such as Bullous Pemphigoid, Pemphigus Vulgaris) and genetic fragility disorders (Epidermolysis Bullosa) characterized by fluid-filled blisters on skin and mucous membranes.",
        "causes": [
            "Autoimmune antibodies targeting hemidesmosomal proteins (BP180, BP230 in Bullous Pemphigoid) or desmogleins (Dsg1, Dsg3 in Pemphigus Vulgaris).",
            "Adverse drug reactions (e.g., penicillamine, ACE inhibitors, DPP-4 inhibitors in elderly patients).",
            "Genetic mutations affecting dermal-epidermal anchoring complexes.",
            "Infectious or toxin-mediated processes."
        ],
        "prevention": [
            "Bullous autoimmune disorders cannot always be prevented, but early detection prevents life-threatening complications.",
            "Review all medications regularly with your physician to identify potential drug-induced blistering triggers.",
            "Prevent secondary mechanical skin trauma by avoiding friction, tight garments, and adhesive bandages.",
            "Handle fragile skin gently using silicone-based medical tapes rather than standard adhesives."
        ],
        "care": [
            "Never deliberately pop, puncture, or de-roof intact blister roofs; the blister roof acts as a natural sterile biological dressing.",
            "Gently cleanse non-ruptured blisters with sterile saline or mild antiseptic wash.",
            "Apply non-adherent sterile dressings (e.g., petrolatum gauze, silicone dressings) to erosions.",
            "Maintain strict hygiene to prevent bacterial superinfections."
        ],
        "treatment": (
            "Requires immediate specialist dermatologist management. Diagnosis is confirmed via skin biopsy for histology and "
            "direct immunofluorescence (DIF). Treatments include systemic corticosteroids, immunosuppressants (mycophenolate, azathioprine), "
            "and anti-CD20 targeted biological therapy (rituximab)."
        ),
        "foods": (
            "If oral mucosal blisters are present, consume soft, bland, room-temperature foods; avoid hot, acidic, crunchy, or spicy items. "
            "Maintain high protein intake to support re-epithelialization of denuded skin."
        ),
        "urgency": (
            "Urgent Emergency: Seek immediate medical care for rapidly spreading blisters, skin detachment, mucosal erosion "
            "(mouth, eyes, genitals), difficulty swallowing, or systemic symptoms like fever and dehydration."
        )
    },

    "Cellulitis Impetigo and other Bacterial Infections": {
        "description": "Bacterial skin infections include superficial impetigo (contagious epidermal sores with honey-colored crusts) and deep spreading cellulitis (dermal and subcutaneous infection typically caused by Streptococcus or Staphylococcus).",
        "causes": [
            "Bacterial invasion by Staphylococcus aureus (including MRSA) or Streptococcus pyogenes.",
            "Break in the epidermal barrier: cuts, abrasions, insect bites, ulcers, fungal toe-web infections (tinea pedis), or surgical wounds.",
            "Venous insufficiency, chronic lymphedema, diabetes mellitus, or impaired immune status.",
            "Direct contact with infected individuals or contaminated surfaces in impetigo."
        ],
        "prevention": [
            "Promptly clean all minor cuts, scrapes, and abrasions with soap and water, applying petroleum jelly and clean bandages.",
            "Treat underlying fungal skin conditions like athlete's foot to eliminate entry portals for bacteria.",
            "Practice frequent, thorough handwashing with soap and warm water.",
            "Do not share personal towels, bed linens, clothing, razors, or athletic gear.",
            "Keep fingernails trimmed short to prevent self-inoculation through scratching."
        ],
        "care": [
            "Elevate the affected limb if cellulitis is present on a leg or arm to reduce swelling.",
            "Wash hands thoroughly before and after touching any dressings or infected skin areas.",
            "Mark the outer boundary of skin redness with a soft surgical pen to track whether the erythema is advancing.",
            "Cover impetigo sores with sterile non-stick dressings to stop transmission to others."
        ],
        "treatment": (
            "Impetigo is treated with topical antibiotics (e.g., mupirocin, retapamulin) or oral antibiotics for extensive disease. "
            "Cellulitis requires prompt oral or intravenous systemic antibiotics (e.g., cephalexin, amoxicillin-clavulanate, clindamycin). "
            "Complete the entire antibiotic course exactly as prescribed even if symptoms improve early."
        ),
        "foods": (
            "Stay well hydrated and maintain a balanced, protein-rich diet to support tissue repair and immune function. "
            "No specific food cures bacterial skin infections."
        ),
        "urgency": (
            "Seek emergency medical evaluation for rapidly spreading redness, severe throbbing pain, red streaks spreading toward the heart, "
            "high fever, chills, confusion, or bullae/blisters over red swollen skin (possible necrotizing fasciitis)."
        )
    },

    "Eczema Photos": {
        "description": "Eczema refers to a spectrum of itchy, erythematous inflammatory dermatitis conditions including nummular eczema, dyshidrotic eczema, and asteatotic eczema, manifesting with dry, scaling, or vesiculated skin.",
        "causes": [
            "Defective epidermal barrier allowing excessive transepidermal water loss (TEWL) and irritant penetration.",
            "Environmental triggers: soaps, detergents, chemicals, cold winds, dry indoor heat, and sweating.",
            "Frequent handwashing or water immersion without immediate re-moisturization.",
            "Stress, psychological anxiety, and immune hyperreactivity."
        ],
        "prevention": [
            "Apply thick emollient ointments or ceramide-rich creams repeatedly throughout the day.",
            "Wear protective nitrile or cotton-lined gloves during housework, dishwashing, or chemical handling.",
            "Bathe with lukewarm water rather than hot showers; use soap-free syndet cleansing bars.",
            "Use fragrance-free laundry detergents and avoid fabric softeners with strong perfumes.",
            "Maintain ambient indoor air humidity using a room humidifier during cold seasons."
        ],
        "care": [
            "Apply moisturizers immediately after patting skin lightly dry with a soft towel.",
            "Apply cool, wet compresses to soothe intense itchy patches without mechanical scratching.",
            "Keep nails smooth and short to prevent skin excoriation and secondary bacterial infections.",
            "Wear loose, soft 100% cotton clothing."
        ],
        "treatment": (
            "Treated topically with mid-to-high potency topical corticosteroids during acute exacerbations, "
            "transitioning to topical calcineurin inhibitors or crisaborole for maintenance. Phototherapy (narrowband UVB) "
            "is effective for generalized recalcitrant eczema."
        ),
        "foods": (
            "Food restrictions rarely resolve generalized adult eczema unless clinical prick or patch testing proves an allergy. "
            "Avoid excessive alcohol and dehydrating beverages; consume a diet high in anti-inflammatory omega-3 fatty acids."
        ),
        "urgency": (
            "Consult a physician if eczema disrupts daily activities or sleep, or if the skin develops oozing crusts, pustules, "
            "fever, or severe pain indicating secondary bacterial or viral infection."
        )
    },

    "Exanthems and Drug Eruptions": {
        "description": "Exanthems are widespread cutaneous eruptions triggered by viral infections (morbilliform exanthem) or adverse drug hypersensitivity reactions (morbilliform drug eruption, DRESS syndrome, Stevens-Johnson syndrome).",
        "causes": [
            "Adverse immune reactions to newly started pharmaceutical drugs (antibiotics, anticonvulsants, NSAIDs, allopurinol).",
            "Systemic viral infections (Enterovirus, EBV, CMV, Parvovirus B19, HHV-6, Measles).",
            "Interaction between viral infection and antibiotic therapy (e.g., amoxicillin in EBV mononucleosis).",
            "Immune-mediated Type IV delayed hypersensitivity reactions."
        ],
        "prevention": [
            "Keep an accurate, written record of all past drug allergies and adverse reactions to show every medical provider.",
            "Never re-take a drug that previously caused a severe cutaneous adverse reaction.",
            "Always disclose all prescription drugs, over-the-counter products, and herbal supplements to your physician.",
            "Maintain routine childhood and adult vaccinations against vaccine-preventable exanthematous viral diseases."
        ],
        "care": [
            "Immediately document the names and starting dates of all medications taken in the past 8 weeks.",
            "Use only bland, gentle moisturizers; avoid applying new fragranced lotions, perfumes, or harsh body washes.",
            "Wear loose, soft cotton clothing to prevent friction over sensitized, inflamed skin.",
            "Take cool baths with colloidal oatmeal to relieve generalized cutaneous discomfort."
        ],
        "treatment": (
            "Drug eruptions require immediate evaluation by a medical doctor to identify and safely discontinue the culprit drug. "
            "Viral exanthems are typically self-limiting and managed symptomatically with oral antihistamines and topical emollients. "
            "Do not stop critical life-sustaining prescription medicines without direct doctor instructions."
        ),
        "foods": (
            "Food avoidance does not treat drug-induced eruptions. Maintain adequate hydration with water and electrolyte fluids. "
            "Avoid introducing exotic new foods during the flare to prevent confounding diagnostic assessments."
        ),
        "urgency": (
            "Medical Emergency: Seek immediate hospital emergency care if the rash accompanies mucosal involvement (blisters on lips, eyes, mouth, genitals), "
            "skin peeling or blistering, facial swelling, shortness of breath, high fever, lymphadenopathy, or dark urine."
        )
    },

    "Hair Loss Photos Alopecia and other Hair Diseases": {
        "description": "Hair disorders range from non-scarring forms like androgenetic alopecia (pattern baldness), alopecia areata (autoimmune patchy loss), and telogen effluvium (stress shedding) to scarring (cicatricial) alopecias.",
        "causes": [
            "Genetic sensitivity of hair follicles to dihydrotestosterone (DHT) in androgenetic alopecia.",
            "Autoimmune T-cell attack targeting hair follicle antigens in alopecia areata.",
            "Physiological or emotional stress, acute illness, surgery, childbirth, or severe nutritional deficits in telogen effluvium.",
            "Thyroid disorders, iron deficiency anemia, or polycystic ovary syndrome (PCOS).",
            "Mechanical traction from tight braids, ponytails, or extensions (traction alopecia).",
            "Inflammatory cicatricial alopecias destroying follicular stem cells (lichen planopilaris, frontal fibrosing alopecia)."
        ],
        "prevention": [
            "Avoid tight hairstyles that put constant traction on hair roots (tight buns, high ponytails, cornrows).",
            "Minimize harsh chemical hair treatments (perms, bleaches, aggressive chemical relaxers) and extreme heat styling.",
            "Manage chronic physical and psychological stress through mindfulness, adequate sleep, and exercise.",
            "Ensure adequate daily dietary intake of protein, iron, zinc, vitamin D, and essential fatty acids.",
            "Seek early dermatological consultation at the first signs of excessive shedding or visible scalp patches."
        ],
        "care": [
            "Use a gentle, sulfate-free shampoo and wide-tooth comb on damp hair to minimize strand breakage.",
            "Pat hair dry with a soft microfiber towel; avoid vigorous rubbing.",
            "Protect exposed scalp areas with broad-spectrum SPF 30+ sunscreen or protective hats.",
            "Avoid aggressive brushing, head scratching, and unverified commercial miracle oils that irritate the scalp."
        ],
        "treatment": (
            "Androgenetic alopecia: Topical or oral minoxidil, 5-alpha reductase inhibitors (finasteride, dutasteride), and low-level laser therapy. "
            "Alopecia areata: Intralesional corticosteroid injections, topical immunotherapy, or oral JAK inhibitors (e.g., baricitinib, ritlecitinib). "
            "Cicatricial alopecia requires urgent anti-inflammatory therapy to halt irreversible follicular scarring."
        ),
        "foods": (
            "Eat a balanced diet rich in lean proteins, legumes, dark leafy greens, eggs, and nuts. "
            "Check serum ferritin, vitamin D, and thyroid panels before starting high-dose supplements, as excess vitamin A or selenium can worsen hair loss."
        ),
        "urgency": (
            "Consult a dermatologist promptly for rapid patchy hair loss, sudden eyebrow or eyelash shedding, "
            "or scalp sensations of burning, itching, tenderness, redness, or scale indicating potential scarring alopecia."
        )
    },

    "Herpes HPV and other STDs Photos": {
        "description": "Infectious dermatological and anogenital manifestations caused by Herpes Simplex Virus (HSV-1, HSV-2), Human Papillomavirus (HPV), Treponema pallidum (Syphilis), and related viral/bacterial sexually transmitted pathogens.",
        "causes": [
            "Direct mucosal or cutaneous transmission of HSV-1/HSV-2 through kissing, sexual intimacy, or viral shedding.",
            "Infection with Human Papillomavirus strains causing genital warts (condyloma acuminata) or cutaneous verrucae.",
            "Bacterial transmission of Treponema pallidum (causing primary painless chancre or secondary papulosquamous syphilis rash).",
            "Microscopic microtrauma in mucosal membranes during contact facilitating pathogen entry."
        ],
        "prevention": [
            "Practice safer sex by using barrier methods (condoms, dental dams) consistently and correctly.",
            "Get vaccinated against HPV (Gardasil 9) to protect against oncogenic and wart-causing HPV strains.",
            "Avoid sexual contact during active outbreaks, prodromal tingling, or when visible blisters or sores are present.",
            "Do not touch or scratch lesions to prevent autoinoculation to other body sites (including fingers and eyes).",
            "Undergo routine screening for sexually transmitted infections when sexually active with new or multiple partners."
        ],
        "care": [
            "Keep the affected area clean and dry; wash hands thoroughly after touching affected skin.",
            "Wear loose-fitting, breathable cotton underwear to minimize friction and moisture accumulation.",
            "Do not pick, pop, or apply harsh unverified acids to sensitive genital or mucosal lesions.",
            "Use cool compresses or sitz baths to alleviate localized discomfort."
        ],
        "treatment": (
            "Herpes: Oral antiviral therapy (valacyclovir, acyclovir, famciclovir) for episodic outbreaks or daily suppressive therapy. "
            "HPV/Genital warts: In-clinic cryotherapy, podophyllotoxin, imiquimod, or surgical excision. "
            "Syphilis: Intramuscular penicillin G benzathine. Prescription therapies must be guided by diagnostic serology and PCR testing."
        ),
        "foods": (
            "Maintain an active, healthy immune system with wholesome foods, fruits, vegetables, and restorative sleep. "
            "Some patients with HSV monitor dietary L-arginine vs. L-lysine balance, though evidence is variable. Avoid alcohol during acute outbreaks."
        ),
        "urgency": (
            "Seek urgent confidential medical care for any new genital sore, painless genital ulcer, eye involvement (corneal pain or redness from HSV keratitis), "
            "difficulty urinating, or rash on palms and soles accompanied by fever and swollen lymph nodes."
        )
    },

    "Light Diseases and Disorders of Pigmentation": {
        "description": "Pigmentary and photodermatological disorders include vitiligo (autoimmune melanocyte destruction), melasma (hormonal hyperpigmentation), post-inflammatory hyperpigmentation (PIH), and photodermatoses (polymorphous light eruption).",
        "causes": [
            "Autoimmune destruction of epidermal melanocytes mediated by CD8+ T cells in vitiligo.",
            "Hormonal stimulation (estrogen, progesterone, pregnancy, oral contraceptives) combined with UV light in melasma.",
            "Cutaneous inflammation or injury triggering excess melanin deposition in post-inflammatory hyperpigmentation.",
            "Immune hypersensitivity reactions provoked by ultraviolet radiation (UVA/UVB) or visible blue light.",
            "Genetic predisposition affecting melanin synthesis and enzymatic pathways."
        ],
        "prevention": [
            "Apply tinted broad-spectrum sunscreen containing iron oxides daily to protect against both UV and visible blue light.",
            "Wear protective wide-brimmed hats and UV-blocking sunglasses when stepping outdoors.",
            "Avoid excessive aggressive mechanical skin exfoliation, harsh chemical peels, or heat treatments that induce PIH.",
            "Promptly treat underlying inflammatory skin conditions like acne and eczema before hyperpigmentation develops.",
            "Seek shade during peak sunlight hours and avoid sunbeds completely."
        ],
        "care": [
            "Adopt a gentle, non-irritating skincare regimen with mild cleansers and barrier-restoring hydrators.",
            "Incorporate skin-brightening ingredients like azelaic acid, niacinamide, tranexamic acid, or vitamin C under guidance.",
            "Do not use unregulated skin-lightening creams that may contain dangerous mercury or clobetasol.",
            "Avoid friction, vigorous rubbing, and aggressive face scrubs on affected skin."
        ],
        "treatment": (
            "Vitiligo: Topical corticosteroids, topical calcineurin inhibitors, phototherapy (narrowband UVB), and topical JAK inhibitors (ruxolitinib). "
            "Melasma: Broad-spectrum sun protection, topical triple-combination cream (hydroquinone, tretinoin, fluocinolone), tranexamic acid, and chemical peels. "
            "Consult a dermatologist for accurate diagnosis and safe management."
        ),
        "foods": (
            "A balanced antioxidant-rich diet containing polyphenols, vitamins C and E, and beta-carotene can support cellular UV defenses, "
            "though diet alone cannot cure pigmentary conditions."
        ),
        "urgency": (
            "Consult a dermatologist if pigment loss spreads rapidly, is accompanied by systemic autoimmune symptoms (fatigue, weight changes, joint pain), "
            "or if a dark pigmented spot demonstrates asymmetry, border irregularity, multiple colors, or evolving size."
        )
    },

    "Lupus and other Connective Tissue diseases": {
        "description": "Autoimmune connective tissue diseases with prominent cutaneous manifestations include Systemic Lupus Erythematosus (malar butterfly rash), Cutaneous Lupus (discoid lupus), Dermatomyositis (heliotrope rash, Gottron papules), and Scleroderma.",
        "causes": [
            "Autoimmune dysregulation where autoantibodies (ANA, anti-dsDNA, anti-Ro/SSA, anti-La/SSB) target nuclear antigens.",
            "Photosensitivity: Ultraviolet radiation induces keratinocyte apoptosis, exposing autoantigens and triggering immune flares.",
            "Genetic susceptibility combined with environmental triggers (viral infections, silica exposure, certain medications).",
            "Microvascular endothelial injury and abnormal immune-complex deposition."
        ],
        "prevention": [
            "Strict, year-round photoprotection: Apply broad-spectrum SPF 50+ daily, reapplying every 2 hours.",
            "Wear sun-protective clothing (UPF 50+), wide-brimmed hats, and UV-filtering films on car and home windows.",
            "Avoid sun exposure completely during peak daylight hours (10:00 AM to 4:00 PM).",
            "Avoid photosensitizing medications (when alternatives exist) and discuss all prescriptions with your rheumatologist.",
            "Stop smoking immediately; tobacco smoking directly reduces the efficacy of antimalarial medications like hydroxychloroquine."
        ],
        "care": [
            "Use gentle, hypoallergenic skin cleansers and moisturizers formulated for hyper-reactive, sensitive skin.",
            "Do not pick, scratch, or scrub discoid plaques or scaly facial rashes to avoid scarring and permanent pigment loss.",
            "Keep hands and feet warm with thermal gloves if Raynaud phenomenon is present.",
            "Keep a symptom log noting sunlight exposure, fatigue levels, and rash flares."
        ],
        "treatment": (
            "Requires multidisciplinary care by a dermatologist and rheumatologist. Treatments include potent topical corticosteroids, "
            "topical calcineurin inhibitors, oral antimalarials (hydroxychloroquine, chloroquine), systemic corticosteroids, "
            "and immunosuppressive/biologic therapies (methotrexate, mycophenolate, belimumab, anifrolumab)."
        ),
        "foods": (
            "Eat an anti-inflammatory Mediterranean-style diet. Avoid alfalfa sprouts and Echinacea supplements, which can stimulate "
            "the immune system and trigger lupus flares. Ensure adequate calcium and vitamin D supplementation to offset sun avoidance and steroid therapy."
        ),
        "urgency": (
            "Urgent: Seek prompt medical attention for rash accompanied by chest pain, shortness of breath, unexplained fever, "
            "joint swelling, frothy urine (proteinuria), severe headaches, or new skin ulcers."
        )
    },

    "Melanoma Skin Cancer Nevi and Moles": {
        "description": "Melanoma is an aggressive malignancy of melanocytes capable of rapid lymphovascular metastasis. Benign melanocytic nevi (moles) and dysplastic nevi are benign or atypical proliferations of melanocytes requiring close clinical surveillance.",
        "causes": [
            "Intermittent intense ultraviolet (UV) radiation exposure and severe blistering sunburns, particularly during childhood.",
            "Oncogenic genetic mutations (e.g., BRAF V600E, NRAS, CDKN2A) driving uncontrolled melanocyte proliferation.",
            "High total nevus count (more than 50 moles) or presence of atypical/dysplastic nevi.",
            "Phenotype: Fair skin (Fitzpatrick types I and II), red or blond hair, light eye color, and inability to tan.",
            "Personal or family history of melanoma in a first-degree relative."
        ],
        "prevention": [
            "Apply broad-spectrum water-resistant SPF 50+ sunscreen every 2 hours when outdoors.",
            "Never use indoor UV tanning beds; indoor tanning increases melanoma risk by up to 75%.",
            "Perform regular monthly self-examinations using the ABCDE criteria:",
            "  • A: Asymmetry (one half does not match the other).",
            "  • B: Border irregularity (scalloped, ragged, or notched edges).",
            "  • C: Color variation (shades of brown, black, white, red, or blue).",
            "  • D: Diameter greater than 6 mm (pencil eraser size) or changing.",
            "  • E: Evolving (any change in size, shape, elevation, bleeding, or itching).",
            "Schedule regular annual total-body skin exams with dermoscopy performed by a dermatologist."
        ],
        "care": [
            "Never attempt to cut, scrape, burn, freeze, or chemically remove a suspicious mole at home.",
            "Protect moles from severe sunburns, repeated clothing friction, and shaving trauma.",
            "Take close-up baseline photos of moles with a ruler for objective monitoring."
        ],
        "treatment": (
            "Suspicious lesions must undergo full-thickness excisional biopsy with narrow margins for histopathological staging. "
            "Confirmed melanoma is treated by wide local excision with defined margins, sentinel lymph node biopsy (SLNB) when indicated, "
            "and targeted therapies (BRAF/MEK inhibitors) or immune checkpoint inhibitors (PD-1/CTLA-4 blockers) for advanced stages."
        ),
        "foods": (
            "Dietary modifications do not replace surgical oncology. Maintain a wholesome, balanced diet rich in antioxidants "
            "and fresh produce to support general immune and cellular health."
        ),
        "urgency": (
            "High Priority: Any mole demonstrating ABCDE changes, rapid growth, spontaneous bleeding, oozing, ulceration, "
            "new pigment streaks under a fingernail, or an 'ugly duckling' lesion distinct from all other moles requires immediate dermatological evaluation."
        )
    },

    "Nail Fungus and other Nail Disease": {
        "description": "Onychomycosis is a fungal infection of the nail plate and bed (primarily caused by dermatophytes), causing discoloration, subungual hyperkeratosis, and onycholysis. Other nail conditions include nail psoriasis, paronychia, and lichen planus.",
        "causes": [
            "Infection by dermatophyte fungi (Trichophyton rubrum, Trichophyton mentagrophytes), yeasts (Candida), or non-dermatophyte molds.",
            "Warm, dark, moist shoe environments promoting fungal spore proliferation.",
            "Spread from untreated athlete's foot (tinea pedis) to adjacent toenails.",
            "Nail trauma, tight footwear, microvascular disease, diabetes mellitus, and older age.",
            "Systemic or inflammatory diseases like psoriasis producing nail pitting and oil drop discoloration."
        ],
        "prevention": [
            "Keep feet clean and completely dry, particularly between the toes after showering.",
            "Wear breathable footwear and change moisture-wicking socks daily or after exercise.",
            "Never walk barefoot in communal public wet areas (gym locker rooms, swimming pools, shared showers).",
            "Disinfect clippers and nail tools before each use; do not share nail care instruments with family members.",
            "Treat athlete's foot (tinea pedis) immediately to prevent fungal migration to the nail bed.",
            "Choose properly fitted shoes that do not pinch or exert pressure on the toenails."
        ],
        "care": [
            "Trim nails straight across and gently file down thickened nail edges.",
            "Avoid wearing occlusive artificial acrylic nails or dense gel polishes over fungal infections.",
            "Dust antifungal powder or spray inside shoes periodically.",
            "Wash athletic footwear and allow shoes to air out thoroughly between uses."
        ],
        "treatment": (
            "Diagnosis should be confirmed via KOH preparation, fungal culture, or nail clipping PCR/PAS stain. "
            "Mild superficial onychomycosis can be treated with topical lacquers (ciclopirox, tavaborole, efinaconazole) for 48 weeks. "
            "Moderate to severe disease requires oral antifungals (terbinafine, itraconazole) with liver enzyme monitoring."
        ),
        "foods": (
            "A balanced diet containing protein, biotin, zinc, and iron supports overall keratin nail plate strength. "
            "Dietary changes alone do not eradicate fungal organisms in the nail bed."
        ),
        "urgency": (
            "Consult a physician, especially if you have diabetes or peripheral vascular disease, as minor nail infections "
            "can lead to serious bacterial cellulitis or foot ulcers. Rapidly darkening nail bands also require evaluation to rule out subungual melanoma."
        )
    },

    "Poison Ivy Photos and other Contact Dermatitis": {
        "description": "Contact dermatitis encompasses allergic contact dermatitis (Type IV cell-mediated allergy from urushiol in poison ivy/oak, nickel, fragrances) and irritant contact dermatitis (direct toxic damage from harsh detergents, solvents, or acids).",
        "causes": [
            "Allergic sensitization to urushiol oil present in poison ivy, oak, and sumac plants.",
            "Exposure to common topical contact allergens: nickel jewelry, fragrance mixtures, preservatives (isothiazolinones), rubber accelerators, hair dyes (PPD).",
            "Irritant exposure to strong acids, alkalis, harsh industrial soaps, rubbing alcohol, or solvents.",
            "Mechanical abrasion or repeated wet-work stripping protective skin barrier lipids."
        ],
        "prevention": [
            "Learn to identify poison ivy ('leaves of three, let them be') and avoid contact with the plant outdoors.",
            "Wear long pants, long sleeves, and heavy vinyl/nitrile gloves when clearing brush, gardening, or hiking in woodlands.",
            "If exposed to poison ivy, immediately wash skin and clothing with degreasing soap and cold water within 15-30 minutes to remove urushiol oil.",
            "Wash contaminated tools, footwear, and pets that may carry oily plant sap on their fur.",
            "Switch to fragrance-free, dye-free personal care items and hypoallergenic nickel-free jewelry if allergic."
        ],
        "care": [
            "Apply cool wet compresses to inflamed, weeping, or itchy skin for 15-20 minutes several times daily.",
            "Use calamine lotion or colloidal oatmeal soaks to alleviate severe pruritus.",
            "Do not scratch or rub the rash; scratching damages the skin and causes secondary bacterial impetiginization.",
            "Wash all clothing worn during outdoor activities in warm soapy water."
        ],
        "treatment": (
            "Localized reactions respond to mid-to-high potency topical corticosteroids applied twice daily for 1-2 weeks. "
            "Widespread or facial poison ivy dermatitis typically requires a tapering 2-3 week course of oral corticosteroids (prednisone). "
            "Oral antihistamines can help manage nighttime itching. Patch testing by an allergist/dermatologist identifies unknown chemical allergens."
        ),
        "foods": (
            "Some individuals sensitized to urushiol may react to cross-reactive items like mango skin or unroasted cashew shells. "
            "Otherwise, general contact dermatitis does not require broad dietary elimination."
        ),
        "urgency": (
            "Urgent: Seek emergency medical attention if the rash affects the eyes, face, mouth, or genitals, "
            "covers more than a quarter of the body, or if you develop fever, facial swelling, or breathing difficulty (especially if smoke from burning brush was inhaled)."
        )
    },

    "Psoriasis pictures Lichen Planus and related diseases": {
        "description": "Chronic papulosquamous dermatoses including plaque psoriasis (autoimmune hyperproliferative keratinization driven by the IL-23/IL-17 axis) and lichen planus (T-cell-mediated inflammatory disorder affecting skin, nails, and mucous membranes).",
        "causes": [
            "Genetic immune system dysregulation involving Th17/IL-23/IL-17 immune signaling cascades in psoriasis.",
            "Koebner phenomenon: development of psoriatic lesions at sites of mechanical skin trauma, cuts, or friction.",
            "Triggers: Streptococcal infections (guttate psoriasis), severe psychological stress, cold weather, and medications (beta-blockers, lithium).",
            "Lichen planus triggers: Autoimmune response to basal keratinocytes, associated with Hepatitis C infection, dental amalgams, or certain drugs."
        ],
        "prevention": [
            "Protect skin from cuts, scratches, sunburns, and harsh scrubbing to prevent Koebnerization.",
            "Manage systemic stress through mind-body techniques, adequate rest, and routine exercise.",
            "Keep skin thoroughly moisturized to prevent painful cracking and scaling of plaques.",
            "Limit alcohol intake and avoid tobacco smoking, which significantly increase psoriasis severity.",
            "Promptly treat throat and respiratory infections that can trigger guttate flares."
        ],
        "care": [
            "Apply thick emollient ointments (petrolatum, ceramides, salicylic acid preparations) daily to soften scale.",
            "Take short warm baths with bath oils or Epsom salts to gently loosen thick silver scales.",
            "Do not aggressively pick or scrape off scales to avoid pinpoint bleeding (Auspitz sign).",
            "Wear loose, soft clothing that does not generate friction on elbows, knees, or the scalp."
        ],
        "treatment": (
            "Psoriasis: Topical corticosteroids, vitamin D analogs (calcipotriene), calcineurin inhibitors, tazarotene, "
            "narrowband UVB phototherapy, oral systemics (methotrexate, apremilast), and targeted biologics (IL-17, IL-23, and TNF-alpha inhibitors). "
            "Lichen planus: Topical or systemic corticosteroids, oral retinoids (acitretin), and phototherapy."
        ),
        "foods": (
            "Follow a nutrient-dense anti-inflammatory Mediterranean diet. Moderate weight loss in overweight individuals has been shown "
            "to substantially reduce psoriasis disease activity and improve response to biologic medications. Avoid excessive alcohol."
        ),
        "urgency": (
            "Seek prompt medical care for widespread generalized redness covering the entire body (erythrodermic psoriasis), "
            "appearance of numerous tiny sterile pustules on red skin (generalized pustular psoriasis, an emergency), or persistent joint pain and morning stiffness (psoriatic arthritis)."
        )
    },

    "Scabies Lyme Disease and other Infestations and Bites": {
        "description": "Cutaneous parasitic infestations (Scabies mite Sarcoptes scabiei), vector-borne bacterial infections (Lyme disease caused by Borrelia burgdorferi from Ixodes tick bites), and arthropod bites/infestations (bedbugs, fleas, lice).",
        "causes": [
            "Infestation by the microscopic mite Sarcoptes scabiei var. hominis burrowing into the stratum corneum.",
            "Transmission of Borrelia burgdorferi spirochetes through the bite of an infected blacklegged deer tick (Ixodes scapularis).",
            "Bites from bedbugs (Cimex lectularius), fleas, chiggers, or lice injecting salivary allergens.",
            "Close skin-to-skin contact, crowded living conditions, or outdoor exposure in tall grass/brush."
        ],
        "prevention": [
            "Lyme prevention: Wear light-colored long clothing, tuck pant legs into socks, apply EPA-registered insect repellent (DEET or picaridin), and treat outdoor clothing with permethrin.",
            "Perform thorough full-body tick checks after spending time outdoors; immediately remove ticks using fine-tipped tweezers.",
            "Scabies prevention: Avoid direct skin-to-skin contact with infested individuals and their personal linens/towels.",
            "If scabies is diagnosed, all household members and close physical contacts must be treated simultaneously, regardless of symptoms.",
            "Wash all bedding, towels, and recently worn clothing in hot water (at least 60°C / 140°F) and dry on high heat."
        ],
        "care": [
            "Items that cannot be washed must be sealed in airtight plastic bags for at least 72 hours to starve mites.",
            "Vacuum mattresses, carpets, and upholstered furniture thoroughly.",
            "Keep nails trimmed short and scrubbed clean to prevent secondary bacterial infection from intense nighttime scratching.",
            "Apply calamine lotion or cool compresses to soothe post-treatment itch."
        ],
        "treatment": (
            "Scabies: Topical permethrin 5% cream applied from neck to toes and left on for 8-14 hours (repeated in 7 days), "
            "or oral ivermectin. Itching may persist for 2-4 weeks post-cure (post-scabetic itch) and is treated with antihistamines. "
            "Lyme disease (Erythema migrans 'bullseye' rash): Prompt oral antibiotics (doxycycline, amoxicillin, or cefuroxime) for 14-21 days."
        ),
        "foods": (
            "No specific food cures parasitic infestations or bacterial tick-borne infections. Stay well hydrated and maintain "
            "a balanced diet to support immune resilience."
        ),
        "urgency": (
            "Seek urgent medical evaluation for expanding 'bulls-eye' circular rashes, sudden facial paralysis (Bell palsy), "
            "severe headache, neck stiffness, heart palpitations, swollen painful joints, or crusted hyperkeratotic lesions in immunocompromised individuals."
        )
    },

    "Seborrheic Keratoses and other Benign Tumors": {
        "description": "Common non-cancerous epidermal growths including seborrheic keratoses (benign clonal proliferation of immature keratinocytes), cherry angiomas, dermatofibromas, and skin tags (acrochordons).",
        "causes": [
            "Normal biological skin aging and cumulative lifetime sun exposure.",
            "Genetic mutations in FGFR3 and PIK3CA genes causing localized benign keratinocyte proliferation.",
            "Strong familial genetic predisposition.",
            "Skin friction in body folds (for skin tags) and microtrauma/arthropod bites (for dermatofibromas)."
        ],
        "prevention": [
            "Seborrheic keratoses are a natural part of genetic skin aging and cannot be entirely prevented.",
            "Practice regular sun protection with daily SPF 30+ sunscreen to reduce cumulative photoaging.",
            "Maintain a healthy body weight and reduce skin-on-skin friction in intertriginous areas to prevent excessive skin tags.",
            "Monitor benign growths periodically so any changing or irregular lesion can be differentiated from skin cancer."
        ],
        "care": [
            "Do not attempt to scrape, pick, cut, or burn off benign tumors with home razor blades or OTC wart acid.",
            "Avoid wearing tight jewelry, collars, or clothing straps that catch and tear protruding growths.",
            "If a growth catches on clothing and bleeds, cleanse gently with mild soap and water and cover with a sterile bandage."
        ],
        "treatment": (
            "Seborrheic keratoses are harmless and do not require treatment unless they become irritated, bleed, or cause cosmetic concern. "
            "In-office removal methods include cryotherapy (liquid nitrogen), curettage, electrodessication, or shave excision. "
            "Any atypical lesion with irregular pigment must be biopsied to rule out melanoma."
        ),
        "foods": (
            "No dietary interventions treat or prevent seborrheic keratoses. General antioxidant-rich nutrition supports overall skin health."
        ),
        "urgency": (
            "Consult a dermatologist if a lesion bleeds spontaneously, changes rapidly in size or color, becomes painful, "
            "or if hundreds of itchy seborrheic keratoses erupt suddenly over weeks (the sign of Leser-Trélat, which may indicate internal malignancy)."
        )
    },

    "Systemic Disease": {
        "description": "Cutaneous manifestations of internal medical diseases, including necrobiosis lipoidica (diabetes), pyoderma gangrenosum (inflammatory bowel disease), erythema nodosum (sarcoidosis, infections), xanthomas (hyperlipidemia), and paraneoplastic dermatoses.",
        "causes": [
            "Underlying metabolic disorders: uncontrolled diabetes mellitus, thyroid diseases, severe hyperlipidemia.",
            "Systemic autoimmune and autoinflammatory conditions: Crohn disease, ulcerative colitis, sarcoidosis, rheumatoid arthritis.",
            "Hematological or internal organ malignancies triggering paraneoplastic cutaneous syndromes.",
            "Chronic liver disease or renal failure leading to pruritus, pigment changes, or calciphylaxis."
        ],
        "prevention": [
            "Undergo comprehensive routine primary care health checkups and blood screenings.",
            "Tightly manage chronic systemic conditions (control blood glucose in diabetes, manage lipid panels, adhere to IBD therapy).",
            "Report any unexplained skin eruptions or non-healing ulcers to your primary physician promptly.",
            "Maintain a healthy lifestyle with smoking cessation, regular physical exercise, and cardiovascular risk reduction."
        ],
        "care": [
            "Treat fragile skin gently; avoid harsh trauma, extreme hot water, and aggressive adhesives.",
            "Keep open sores clean and apply clinician-recommended barrier dressings.",
            "Document the timeline of all skin lesions in relation to internal symptoms (fever, bowel habits, weight loss, joint aches)."
        ],
        "treatment": (
            "Therapy must target the underlying systemic etiology. Dermatological symptoms often resolve or improve once the primary "
            "internal disease is managed. Skin-directed therapies include wound care, localized anti-inflammatories, or systemic immunomodulators. "
            "A biopsy with clinicopathological correlation is usually necessary."
        ),
        "foods": (
            "Dietary management depends directly on the diagnosed systemic condition (e.g., low-glycemic diabetic meal planning, "
            "low-cholesterol heart-healthy diet for xanthomas, low-FODMAP/anti-inflammatory diet for inflammatory bowel disease)."
        ),
        "urgency": (
            "Urgent: Seek immediate medical evaluation for rapidly expanding painful ulcers with violaceous borders (pyoderma gangrenosum), "
            "tender red nodules on the shins with fever, skin necrosis, or skin lesions associated with unexplained weight loss and night sweats."
        )
    },

    "Tinea Ringworm Candidiasis and other Fungal Infections": {
        "description": "Superficial cutaneous fungal infections including dermatophytosis (Tinea corporis/ringworm, Tinea cruris/jock itch, Tinea pedis/athlete's foot), candidiasis (Candida albicans in body folds), and pityriasis versicolor (Malassezia).",
        "causes": [
            "Dermatophyte fungi (Trichophyton, Microsporum, Epidermophyton) feeding on dead keratin in skin and hair.",
            "Overgrowth of opportunistic yeast (Candida albicans) in warm, moist, macerated skin folds.",
            "Warm, humid environmental conditions and prolonged sweating.",
            "Direct contact with infected individuals, household pets (cats/dogs with ringworm), or gym equipment.",
            "Immune compromise, broad-spectrum antibiotic use, or corticosteroid overuse."
        ],
        "prevention": [
            "Keep all skin folds (groin, axillae, under breasts) and feet clean, dry, and well-ventilated.",
            "Change out of sweaty workout clothes, gym attire, and damp socks immediately after physical activity.",
            "Never share personal towels, clothing, combs, footwear, or bedsheets.",
            "Wear shower sandals in communal locker rooms, public showers, and pool areas.",
            "Take domestic pets to the veterinarian if they exhibit circular bald patches or scaly skin.",
            "Dry thoroughly with a clean towel after bathing, drying the unaffected areas before infected areas."
        ],
        "care": [
            "Wash affected skin gently with mild soap and pat thoroughly dry with a dedicated towel.",
            "Wear loose, breathable 100% cotton clothing to prevent moisture buildup in intertriginous areas.",
            "Do not apply hydrocortisone or steroid creams to fungal infections (steroids mask symptoms and feed fungal growth — 'tinea incognito').",
            "Wash contaminated clothing and gym gear in hot water."
        ],
        "treatment": (
            "Localized dermatophytosis and candidiasis respond well to topical antifungals (terbinafine, clotrimazole, miconazole, ketoconazole) "
            "applied twice daily, extending 1-2 cm beyond the active border for at least 2-4 weeks. Extensive tinea, scalp tinea (tinea capitis), "
            "or recalcitrant cases require oral antifungals (terbinafine, itraconazole, fluconazole) under medical supervision."
        ),
        "foods": (
            "Limit excessive refined sugar and alcohol intake, particularly for recurring candidiasis. Maintain adequate hydration "
            "and a balanced, whole-food diet to support natural immune defenses."
        ),
        "urgency": (
            "Seek medical care if the rash spreads across large body areas, does not improve after 2 weeks of OTC antifungal therapy, "
            "involves the scalp or beard area, or develops secondary bacterial infection (pus, increasing heat, spreading redness, fever)."
        )
    },

    "Urticaria Hives": {
        "description": "Urticaria (hives) is characterized by transient, highly pruritic, erythematous edematous wheals with central pallor caused by mast cell degranulation and histamine release in the superficial dermis.",
        "causes": [
            "Mast cell degranulation releasing histamine, prostaglandins, and leukotrienes causing localized vasodilation and vascular permeability.",
            "IgE-mediated Type I allergic triggers: foods (shellfish, nuts), medications (penicillin, NSAIDs), insect stings, latex.",
            "Non-allergic physical triggers: pressure (dermatographism), heat, cold, exercise, vibration, sunlight (solar urticaria).",
            "Acute viral or bacterial infections (especially in children).",
            "Autoimmune urticaria with autoantibodies targeting the high-affinity IgE receptor (FcεRI) or IgE itself."
        ],
        "prevention": [
            "Strictly avoid identified food allergens, culprit medications (such as NSAIDs/aspirin, which can directly provoke mast cells), and known physical triggers.",
            "Avoid hot showers, overheated rooms, tight constricting clothing, and intense friction during flare-ups.",
            "Manage emotional stress, as acute stress triggers neurogenic histamine release.",
            "Keep an accurate symptom and food/medication diary to identify potential recurring triggers.",
            "Carry non-sedating oral antihistamines and an epinephrine auto-injector if past episodes included systemic anaphylaxis."
        ],
        "care": [
            "Apply cool, soothing compresses or take cool baths with colloidal oatmeal to relieve the intense itch.",
            "Wear loose, smooth, lightweight cotton clothing to avoid friction against sensitive skin.",
            "Avoid scratching wheals, as friction triggers the release of additional histamine.",
            "Rest in a cool, well-ventilated, quiet room."
        ],
        "treatment": (
            "First-line treatment consists of second-generation non-sedating H1 antihistamines (cetirizine, fexofenadine, loratadine, bilastine) "
            "at standard or up-titrated doses under medical supervision. Severe refractory chronic spontaneous urticaria responds to "
            "the monoclonal anti-IgE antibody omalizumab or immunosuppressive agents like cyclosporine."
        ),
        "foods": (
            "If a specific food allergy is clinically confirmed, avoid that food strictly. For pseudo-allergic chronic hives, some patients "
            "benefit from minimizing high-histamine foods (aged cheeses, cured meats, fermented products, wine) under dietitian guidance."
        ),
        "urgency": (
            "Medical Emergency: Seek immediate 911 / emergency department care if hives are accompanied by swelling of the lips, tongue, or throat "
            "(angioedema), difficulty breathing, wheezing, dizziness, throat tightness, or collapse (anaphylaxis)."
        )
    },

    "Vascular Tumors": {
        "description": "Benign and malignant proliferations of blood and lymphatic vessels, including infantile hemangiomas, pyogenic granulomas, cherry angiomas, glomus tumors, and Kaposi sarcoma.",
        "causes": [
            "Endothelial cell hyperplasia and abnormal angiogenic signaling (VEGF, basic fibroblast growth factor).",
            "Infantile hemangiomas arise from dysregulated placental or vascular progenitor cells during early fetal life.",
            "Pyogenic granulomas are often triggered by localized trauma, chronic irritation, or hormonal surges (pregnancy).",
            "Kaposi sarcoma is caused by Human Herpesvirus 8 (HHV-8) infection, primarily in the setting of immunosuppression or HIV.",
            "Cherry angiomas are normal, benign aging-related vascular ectasias with strong genetic predisposition."
        ],
        "prevention": [
            "Benign vascular anomalies like hemangiomas and cherry angiomas cannot be prevented as they are congenital or genetic.",
            "Protect skin from localized physical trauma and picking to prevent bleeding pyogenic granulomas.",
            "Practice safe sex and maintain immune health to reduce the risk of HHV-8 transmission and Kaposi sarcoma.",
            "Shield prominent vascular lesions from direct sun exposure with SPF 30+ sunscreen."
        ],
        "care": [
            "Do not scratch, puncture, or pick at vascular lesions, as they bleed easily and profusely.",
            "If a vascular growth bleeds, apply firm, continuous direct pressure with a clean sterile gauze for 10-15 minutes.",
            "Keep the lesion clean and protect protruding nodules with a soft protective bandage.",
            "Monitor infantile hemangiomas for ulceration or rapid growth near eyes, mouth, or airway."
        ],
        "treatment": (
            "Infantile hemangiomas requiring intervention (e.g., obstructing vision or breathing) are treated with oral propranolol or topical timolol. "
            "Pyogenic granulomas and cherry angiomas are safely removed in clinic via shave excision with cautery, pulsed dye laser (PDL), or cryotherapy. "
            "Kaposi sarcoma requires antiretroviral therapy (ART) and oncological management."
        ),
        "foods": (
            "Dietary modifications do not alter vascular proliferation or treat vascular lesions. Maintain a wholesome, balanced diet."
        ),
        "urgency": (
            "Consult a physician promptly for vascular lesions that bleed repeatedly, ulcerate, grow rapidly, obstruct vision or breathing in infants, "
            "or present as multiple purple-brown patches or nodules in adults (suspicion of Kaposi sarcoma or angiosarcoma)."
        )
    },

    "Vasculitis Photos": {
        "description": "Cutaneous vasculitis is characterized by inflammation and destruction of dermal blood vessel walls, presenting typically as palpable purpura, petechiae, livedo reticularis, or painful cutaneous ulcers.",
        "causes": [
            "Deposition of circulating immune complexes in post-capillary venule walls (Leukocytoclastic vasculitis / IgA vasculitis).",
            "Hypersensitivity reactions to medications (antibiotics, NSAIDs, thiazides, propylthiouracil).",
            "Systemic autoimmune diseases (Systemic Lupus Erythematosus, Rheumatoid Arthritis, ANCA-associated vasculitides).",
            "Systemic infections: Hepatitis B, Hepatitis C, HIV, Streptococcal infections, or subacute bacterial endocarditis.",
            "Underlying hematological or solid organ malignancies."
        ],
        "prevention": [
            "Review and avoid known culprit medications that have previously triggered hypersensitivity vasculitis.",
            "Avoid prolonged standing and strenuous leg exercise during active purpuric flares.",
            "Protect legs from cold temperatures and mechanical friction with warm, soft clothing.",
            "Manage underlying chronic autoimmune or viral diseases (e.g., treating Hepatitis C with direct-acting antivirals)."
        ],
        "care": [
            "Elevate lower extremities above heart level as much as possible to decrease venous hydrostatic pressure and purpura.",
            "Avoid tight socks with elastic bands that cut into the skin; wear loose, comfortable garments.",
            "Gently clean fragile purpuric or ulcerated areas and dress with non-stick sterile dressings.",
            "Avoid scratching, rubbing, or applying irritating OTC ointments to non-blanching purple spots."
        ],
        "treatment": (
            "Comprehensive diagnostic evaluation is required, including punch biopsy for histology and direct immunofluorescence (DIF), "
            "urinalysis, serum creatinine, and autoimmune panels. Treatment involves stopping offending medications, systemic corticosteroids "
            "(prednisone), colchicine, dapsone, or steroid-sparing immunosuppressants (methotrexate, azathioprine, rituximab)."
        ),
        "foods": (
            "Maintain a low-sodium, heart-healthy diet to minimize peripheral edema, especially if systemic corticosteroids are prescribed. "
            "Stay well hydrated and avoid excessive alcohol."
        ),
        "urgency": (
            "Urgent: Seek immediate medical evaluation for palpable purpura accompanied by abdominal pain, blood in stool or urine, "
            "shortness of breath, chest pain, joint swelling, fever, or painful rapidly expanding skin necrosis and ulcers."
        )
    },

    "Warts Molluscum and other Viral Infections": {
        "description": "Benign epidermal viral infections including verruca vulgaris (common warts), plantar warts, and flat warts caused by Human Papillomavirus (HPV), as well as Molluscum Contagiosum caused by the Molluscipoxvirus.",
        "causes": [
            "Infection of the basal epidermal layer by Human Papillomavirus (HPV types 1, 2, 4, 27, 57).",
            "Infection by Molluscum Contagiosum Virus (MCV), a member of the Poxviridae family, causing umbilicated pearly papules.",
            "Direct person-to-person skin contact or sexual transmission.",
            "Indirect fomite transmission via gym mats, shared towels, locker room floors, toys, or swimming pools.",
            "Autoinoculation: scratching, picking, nail biting, or shaving spreads the virus to adjacent skin."
        ],
        "prevention": [
            "Do not pick, scratch, bite, or shave over warts or molluscum bumps to prevent autoinoculation.",
            "Wear waterproof sandals or flip-flops in public showers, locker rooms, and around communal pool decks.",
            "Never share towels, washcloths, razors, nail clippers, or clothing with an infected person.",
            "Wash hands thoroughly after touching or treating warts.",
            "Cover active lesions with waterproof bandages or clothing during sports, swimming, and physical contact."
        ],
        "care": [
            "Keep the affected skin clean and dry; do not share bathwater with siblings in childhood molluscum.",
            "Avoid walking barefoot on home carpets and hardwood floors if plantar warts are present.",
            "Do not attempt aggressive self-surgery with blades, needles, or nail clippers.",
            "Cover warts with medical tape or bandages to reduce the urge to pick and limit viral shedding."
        ],
        "treatment": (
            "Warts: Topical salicylic acid with gentle debridement, in-clinic cryotherapy (liquid nitrogen), cantharidin, "
            "intralesional Candida antigen, or pulsed dye laser. Molluscum: Often self-resolves over 6-18 months in healthy children; "
            "active therapies include topical cantharidin, cryotherapy, curettage, or topical potassium hydroxide."
        ),
        "foods": (
            "A balanced, nutrient-rich diet supports natural cell-mediated immunity, which is ultimately responsible for clearing the viral infection. "
            "No specific food cures viral warts directly."
        ),
        "urgency": (
            "Consult a dermatologist if warts are painful, interfere with walking or daily function, bleed easily, "
            "multiply rapidly, occur on the genital area, or appear in an immunocompromised individual."
        )
    },

    "Clear & Healthy Skin": {
        "description": "Visual analysis indicates clear, healthy skin with no clinical signs of acute inflammatory rashes, active infections, or suspicious neoplastic lesions.",
        "causes": [
            "Intact epidermal skin barrier function and balanced lipid stratum corneum.",
            "Healthy physiological skin cell turnover without hyperkeratinization or follicular plugging.",
            "Absence of active bacterial, fungal, or viral pathogen proliferation.",
            "Balanced cutaneous immune response with no active autoimmune inflammatory flares."
        ],
        "prevention": [
            "Maintain daily broad-spectrum sun protection with SPF 30+ or higher to prevent premature photoaging and UV DNA damage.",
            "Cleanse gently twice daily with a mild, pH-balanced, non-stripping cleanser.",
            "Keep the skin barrier resilient by applying hydrating ceramide- or hyaluronic acid-based moisturizers.",
            "Avoid excessive physical scrubbing or harsh chemical peels that compromise the protective lipid barrier.",
            "Perform regular monthly self-examinations to monitor for any new, evolving, or changing moles (ABCDE criteria)."
        ],
        "care": [
            "Wash with lukewarm water rather than hot water to prevent trans-epidermal water loss.",
            "Apply moisturizer while skin is still slightly damp after showering to lock in essential hydration.",
            "Choose non-comedogenic skincare products and clean makeup tools and pillowcases regularly.",
            "Stay well hydrated throughout the day and get adequate restorative sleep for cellular skin repair."
        ],
        "treatment": (
            "No medical treatment is required. Your skin exhibits clear, healthy characteristics. "
            "Continue your regular preventive skincare and sun protection regimen. "
            "Schedule an annual routine clinical skin examination with a board-certified dermatologist for preventive wellness."
        ),
        "foods": (
            "Support your natural skin health with an antioxidant-rich diet containing colorful vegetables, berries, "
            "omega-3 fatty acids (salmon, walnuts, flaxseeds), zinc, and vitamins C and E. Drink plenty of fresh water daily."
        ),
        "urgency": (
            "Routine / Normal: No urgent clinical intervention is indicated. "
            "Consult a dermatologist if you notice any new rapidly growing spots, changing moles, or persistent irritation in the future."
        )
    },

    "Clear Skin": {
        "description": "Visual analysis indicates clear, healthy skin with no clinical signs of acute inflammatory rashes, active infections, or suspicious neoplastic lesions.",
        "causes": [
            "Intact epidermal skin barrier function and balanced lipid stratum corneum.",
            "Healthy physiological skin cell turnover without hyperkeratinization or follicular plugging.",
            "Absence of active bacterial, fungal, or viral pathogen proliferation.",
            "Balanced cutaneous immune response with no active autoimmune inflammatory flares."
        ],
        "prevention": [
            "Maintain daily broad-spectrum sun protection with SPF 30+ or higher to prevent premature photoaging and UV DNA damage.",
            "Cleanse gently twice daily with a mild, pH-balanced, non-stripping cleanser.",
            "Keep the skin barrier resilient by applying hydrating ceramide- or hyaluronic acid-based moisturizers.",
            "Avoid excessive physical scrubbing or harsh chemical peels that compromise the protective lipid barrier.",
            "Perform regular monthly self-examinations to monitor for any new, evolving, or changing moles (ABCDE criteria)."
        ],
        "care": [
            "Wash with lukewarm water rather than hot water to prevent trans-epidermal water loss.",
            "Apply moisturizer while skin is still slightly damp after showering to lock in essential hydration.",
            "Choose non-comedogenic skincare products and clean makeup tools and pillowcases regularly.",
            "Stay well hydrated throughout the day and get adequate restorative sleep for cellular skin repair."
        ],
        "treatment": (
            "No medical treatment is required. Your skin exhibits clear, healthy characteristics. "
            "Continue your regular preventive skincare and sun protection regimen. "
            "Schedule an annual routine clinical skin examination with a board-certified dermatologist for preventive wellness."
        ),
        "foods": (
            "Support your natural skin health with an antioxidant-rich diet containing colorful vegetables, berries, "
            "omega-3 fatty acids (salmon, walnuts, flaxseeds), zinc, and vitamins C and E. Drink plenty of fresh water daily."
        ),
        "urgency": (
            "Routine / Normal: No urgent clinical intervention is indicated. "
            "Consult a dermatologist if you notice any new rapidly growing spots, changing moles, or persistent irritation in the future."
        )
    }
}


def normalize_label(label):
    """Normalize label string for consistent dictionary matching."""
    return " ".join(str(label).strip().casefold().split())


_NORMALIZED_RECOMMENDATIONS = {
    normalize_label(name): advice
    for name, advice in SKIN_RECOMMENDATIONS.items()
}


def get_recommendations(predicted_class):
    """
    Return comprehensive educational advice, causes, and prevention
    for the predicted disease category.
    """
    key = normalize_label(predicted_class)

    if key in _NORMALIZED_RECOMMENDATIONS:
        return _NORMALIZED_RECOMMENDATIONS[key]

    return {
        "description": f"Preliminary classification for category: {predicted_class}.",
        "causes": [
            "Specific etiology depends on accurate clinical diagnosis by a healthcare professional.",
            "Skin conditions commonly arise from infections, immune dysregulation, environmental allergens, or genetics."
        ],
        "prevention": [
            "Maintain proper skin hygiene with mild, fragrance-free cleansers.",
            "Protect skin from excessive UV exposure with daily broad-spectrum SPF 30+ sunscreen.",
            "Avoid scratching, picking, or traumatizing affected skin.",
            "Consult a board-certified dermatologist for an accurate diagnostic assessment."
        ],
        "care": [
            "Use gentle, hypoallergenic skin-care products and avoid harsh physical scrubbing.",
            "Keep the affected skin area clean, dry, and protected from environmental irritants."
        ],
        "treatment": (
            f"No specific automated guidance is available for '{predicted_class}'. "
            "Please schedule an in-person clinical examination with a qualified dermatologist."
        ),
        "foods": (
            "Maintain a balanced, nutrient-dense diet and stay well hydrated. Avoid foods only for confirmed allergies."
        ),
        "urgency": (
            "Seek urgent medical evaluation for rapidly spreading redness, severe pain, extensive blistering, "
            "fever, or difficulty breathing."
        )
    }
