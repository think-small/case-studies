from app import db, Units, CaseUnitMapper, CaseTestResults, CaseNotes

def add(obj):
    db.session.add(obj)
    db.session.commit()

db.create_all()

#  Create Units Table
osmo = Units(unit = "Osmolality and Electrolytes")
renal = Units(unit = "Renal Physiology")
lipids = Units(unit = "Apolipoprotein Metabolism")
hepatitis_hiv = Units(unit = "Viral Hepatitis and HIV")
enzymes = Units(unit = "Enzymology")

add(osmo)
add(renal)
add(lipids)
add(hepatitis_hiv)
add(enzymes)

#  Case 1 -SIADH
case_1 = CaseUnitMapper(caseID = 1, unitID = 1, unit = osmo)
add(case_1)

case_1_sodium = CaseTestResults(testName = "sodium", lowerBound = 110, upperBound = 125, case = case_1)
case_1_osmolality = CaseTestResults(testName = "osmolality", lowerBound = 245, upperBound = 265, case = case_1)
case_1_urine_osmo = CaseTestResults(testName = "osmolality, urine", lowerBound = 315, upperBound = 335, case = case_1)
case_1_urine_sodium = CaseTestResults(testName = "sodium, urine", lowerBound = 80, upperBound = 120, case = case_1)
case_1_glucose = CaseTestResults(testName = "glucose", lowerBound = 120, upperBound = 160, case = case_1)
case_1_co2 = CaseTestResults(testName = "CO2", lowerBound = 20, upperBound = 24, case = case_1)
case_1_chloride = CaseTestResults(testName = "chloride", lowerBound = 90, upperBound = 95, case = case_1)

add(case_1_sodium)
add(case_1_osmolality)
add(case_1_urine_osmo)
add(case_1_urine_sodium)
add(case_1_glucose)
add(case_1_co2)
add(case_1_chloride)

case_1_note_1 = CaseNotes(note = "Note number one", noteType = "progress", case = case_1)
case_1_note_2 = CaseNotes(note = "Note number two", noteType = "vitals", case = case_1)
case_1_note_3 = CaseNotes(note = "Note number three", noteType = "physical_exam", case = case_1)

add(case_1_note_1)
add(case_1_note_2)
add(case_1_note_3)