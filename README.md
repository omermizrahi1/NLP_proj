# מיני פרוייקט בעיבוד שפה טבעית
# בניין נפעל

## הוראות קריאת הפרויקט:

הפרויקט יחולק לשני branches
- הפעלים מהתנ"ך - Tanach_window
- הפעלים מויקפידיה העברית - Wiki_window

כאשר בכל אחד מהענפים יהיו שתי מחברות יופיטר רלוונטיות:
-עבור קוד המודל, האימון והתוצאות - trainedmodels.ipynb.
-עמוד סטטיסטיקות על המידע שניתחנו - datastatistics.ipynb.


## בחירת הטקסטים

כשעברנו על הטקסטים בשני הקורפוסים, ראינו שיש הרבה טקסטים מתחום המשפט, ולכן חשבנו לבחור טקסטים מקבילים מהתנ"ך שהם קשורים למשפט גם כן. בחרנו בטקסטים מהתורה ובפרט מספרי שמות, ויקרא, במדבר, כי שם יש טקסטים בעלי אופי משפטי – חוקים. 
בדיעבד לאחר משימת תיוג הטקסטים לדעתנו הבחירה בטקסטים אלו הייתה שגויה, משום שאם היינו בוחרים טקסטים יותר מגוונים היינו יכולים לקבל תוצאות טובות יותר באופן כללי מכלל התנ"ך, שכן בטקסטים שבחרנו מהתנ"ך יש פעלים רבים ותבניות שחוזרות על עצמן.

## עיבוד הטקסטים
כדי להתחיל במשימת התיוג היה עלינו לשלוף מהקורפוסים שבחרנו את הפעלים הרלוונטיים לפי הבניין שבחרנו.
עשינו זאת בעזרת הסקריפטים tanachparser.py ו- wikiparser.py. 

## בניית מדריך התיוג

בבניית מדריך התיוג נעזרנו בספרים של הבלשנים. ההסברים של גלינרט היה די ברור ומפורט עם דוגמאות ברורות, לעומת ההסברים של בלאו שהיו מעט פשטניים מדי לדעתנו. את מדריך התיוג ניתן לראות בקובץ tagging_manual.pdf.

## תיוג הדוגמאות
תחילה התיוג היה מאוד מבלבל, אך עם ההתקדמות זה בא יותר בקלות. שיטת התיוג של גלינרט הייתה יותר קלה וברורה מאשר של בלאו, החלוקה הייתה יותר הגיונית. כמו כן, בשני השיטות יש תיוגים שברובם היו חופפים (לדוגמא תיוג 5 בשני השיטות, תיוג 1 ו2 בגלינרט היה חופף לתיוג 3 בבלאו, ותיוג 4 בשני המקרים). כמו כן, כפי שנראה בסטטיסטיקות על ה-dataset, פיזור התיוג היה לא מאוזן בכלל. דבר שיכול להשפיע על תוצאות המסווג – נראה זאת בהמשך.


## סטטיסטיקות על הדאטה

אספנו מספר סטטיסטיקות שיכולות ללמד אותנו על טיב ה- data שאספנו. את הסטטיסטיקות הללו ניתן למצוא במחברת datastatistics.ipynb בכל ענף.

## בניית וקטור הדוגמאות

החלטנו שכדי לקבל יותר מידע על הפעלים שברשותנו, אנחנו צריכים לדעת את הקונטקסט של כל פועל. לכן, כתבנו מתודות אשר בהינתן פועל  וגודל חלון, נותנות לנו את כל המילים שלפני ואחרי המילה כגודל החלון (לדוג', אם גודל החלון הוא 2, ניקח 2 מילים לפניה ו - 2 מילים אחריה במשפט).
לכל פועל מכל הפעלים המתויגים, כתבנו את כל הנתונים הסינטקטיים והמורפולוגים לכל מילה אשר נמצאת בחלון. את נתוני הווקטור ניתן לראות בקובץ merged.xlsx. <br>
לאחר מכן החלטנו, שנשווה את הווקטורים שהוצאנו עם גודל החלון לשיפור נוסף שהוצע בהנחיות העבודה: קומבינציות בין המאפיינים השונים של כל מילה ולכן, הוספנו לכל וקטור הרכבים של מאפיינים עבור כל מילה בחלון. 
את ווקטורי המאפיינים האלה ניתן לראות בקבצים: merged_comb_blau.xlsx ו-merged_comb_glinert.xlsx. <br>
לאחר מכן, כאשר אימנו את המודל השתמשנו ב - OneHotEncoder מספריית scikit-learn לקודד את ה - data, משום שהדאטה הוא ברובו קטגורי.
בהמשך נראה שהווקטור בעל ההרכבים של קומבינציות המאפיינים קיבל תוצאות טובות יותר במקצת.
את פונקציונליות זו ניתן לראות בקבצים pds.py, feature_vector.py.<br>
בעיה שצצה לנו תוך כדי היא שרצינו לאחד את שני ה - datasets, אך המאפיינים הסינטקטיים של שני המאגרים מתויגים באופן שונה מה שהקשה על ההשוואה בין השניים. 
שימוש במאפיינים הסינטקטיים נותן מידע רב על הקונטקסט של הפועל עליו נרצה לעשות קלסיפקציה. אם, למשל, היה לנו את התנ"ך מתוייג בפורמט conllu, דבר זה היה מתאפשר. לכן החלטנו לפצל את הדאטסטים ולהכין 2 מודלים, אחד לכל גישת תיוג לכל קורפוס. 
כמו כן, חששנו שסגנון הכתיבה השונה "יבלבל" את המודל וישפיע לרעה על תוצאות הסיווג. לכן, לבסוף החלטנו להפריד בין שני הקורפוסים.

## אימון המסווג

תחילה הפרדנו את ה - data למדגם אימון ומדגם מבחן (train, test). לאחר מכן השתמשנו בספרייה [Lazy Predict](https://lazypredict.readthedocs.io/en/latest/usage.html#classification) כדי לבחור את המודל עם מדד ה - accuracy הגבוה ביותר על מדגם ה - test. את התוצאות ניתן לראות בקובץ lazypredict_results.txt שבתיקיית logs.
קורפוס התנ"ך
- עבור גלינרט ללא הרכב מאפיינים המודל הכי טוב שקיבלנו הוא [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- עבור בלאו ללא הרכב מאפיינים המודל הכי טוב שקיבלנו הוא [XGBoost](https://xgboost.readthedocs.io/en/stable/python/python_api.html)
- עבור גלינרט עם הרכב מאפיינים המודל הכי טוב שקיבלנו הוא [Extra Trees](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html)
- עבור בלאו עם הרכב מאפיינים המודל הכי טוב שקיבלנו הוא [Extra Trees](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html)

קורפוס ויקיפדיה העברית
- עבור גלינרט ללא הרכב מאפיינים המודל הכי טוב שקיבלנו הוא.
- עבור בלאו ללא הרכב מאפיינים המודל הכי טוב שקיבלנו הוא 
- עבור גלינרט עם הרכב מאפיינים המודל הכי טוב שקיבלנו הוא 
- עבור בלאו עם הרכב מאפיינים המודל הכי טוב שקיבלנו הוא

לאחר מכן החלטנו לקחת את המודל שהניב את המדדים הכי טובים בכל גישה, ולעשות לו hyperparameters tuning ו- 10 fold cross validation. זאת עשינו בעזרת ספריית [Optuna](https://optuna.org/), המשמשת לאופטימיזציה של היפר פרמטרים, תוך שימוש באופטימיזציה מבוססת SMBO כדי לחפש ביעילות את ערכי הhyperparameters הטובים ביותר. את תוצאות ההרצה ניתן לראות בקבצי הלוגים אשר נמצאים בתיקיית logs.
לאחר הרצת optuna רצינו לבדוק האם באמת ה Hyperparameter tuning  נתנה לנו תוצאות טובות. הרצנו את המתודה test_optimiztion אשר נמצאת במחברת trainedmodel.ipynb. ניתן לראות שעבור המודלים שאימנו על קורפוס התנ"ך היה שיפור, אם כי שיפור מינורי. להשלים על ויקי.


## תוצאות

תוצאות:
את תוצאות האימון ניתן לראות בקובץ trainedmodel
אפשר לראות שהתוצאות שקיבלנו לא מדהימות. הנה כמה סיבות אפשריות לכך:
- דאטה סט קטן מידי – 500~ דוגמאות זה מספר מעט מידי של דוגמאות.
- דוגמאות לא מאוזנות. כפי שניתן לראות בסטטיסטיקות שהוצאנו על ה - data, לכל גישה יש 2 תיוגים שמהוות את רוב התיוגים בעוד שיש תיוגים שכמעט ולא מופיעים.
- תיוגים לא נכונים – שיטת התיוג היא מבלבלת ואינה חד משמעית לכן, איכות הסיווג הוא בסימן שאלה מהסיבה העיקרית שאין לנו ניסיון כבלשנים לסווג מידע ולכן ישנה סבירות שטעינו בחלק מהתיוגים.

