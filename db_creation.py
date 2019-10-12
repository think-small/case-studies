from app import db, Units, CaseUnitMapper, CaseTestResults, CaseNotes, CaseHistory

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

case_1_note_1 = CaseNotes(note = "ED - April 11 2019\n 28 year old female presents to the ER complaining of progressively worsening headaches for 5 days. Patient has noticably slurred speech and difficulty walking. Denies tobacco and alcohol use. Denies illicit drug use. Eating and exercise habits are normal. Denies any missed insulin doses. No other medications besides insulin.", noteType = "history", location = "ED", date = "Thurs April 11 2019 11:15:17", case = case_1)
case_1_note_2 = CaseNotes(note = "ED - April 11 2019\n Temperature: 37.1C, BP: 114 / 72, HR: 83, POC glucose: 105", noteType = "vitals", location = "ED", date = "April 11 2019 11:18:25", case = case_1)
case_1_note_3 = CaseNotes(note = "ED - April 11 2019\n Physical exam: normal findings. No masses or lesions, no organomegaly. No peripheral edema.\nNeurologic exam: impaired physical coordination - abnormal gait. No obvious signs of trauma, no pain with movement. Slurred speech with no signs of stroke or CNS injury.", noteType = "exam", location = "ED", date = "April 11 2019, 11:49:01", case = case_1)
add(case_1_note_1)
add(case_1_note_2)
add(case_1_note_3)

case_1_history_1 = CaseHistory(diagnosis = "Small cell lung cancer", date = "Thurs April 23 2015, 12:06:19", reference = "https://my.clevelandclinic.org/health/articles/6202-small-cell-lung-cancer", reference_name = "Cleveland Clinic - SCL", case = case_1)
case_1_history_2 = CaseHistory(diagnosis = "Diabetes Mellitus, Type II", date = "Sat July 07 2012, 17:21:48", reference = "https://www.mayoclinic.org/diseases-conditions/type-2-diabetes/symptoms-causes/syc-20351193", reference_name = "Mayo Clinic - DM II", case = case_1)
case_1_history_3 = CaseHistory(diagnosis = "Cholecystectomy due to cholelithiasis", date = "Fri November 06 2009, 09:22:00", reference = "https://www.hopkinsmedicine.org/health/treatment-tests-and-therapies/cholecystectomy", reference_name = "Johns Hopkins - Cholecystectomy", case = case_1)
add(case_1_history_1)
add(case_1_history_2)
add(case_1_history_3)