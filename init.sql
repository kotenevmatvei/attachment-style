CREATE OR REPLACE FUNCTION calculate_you_attachment_scores()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculate average scores for the new or updated row
    NEW.anxious_score := (
        NEW.anxious_q1 + NEW.anxious_q2 + NEW.anxious_q3 + NEW.anxious_q4 +
        NEW.anxious_q5 + NEW.anxious_q6 + NEW.anxious_q7 + NEW.anxious_q8 +
        NEW.anxious_q9 + NEW.anxious_q10 + NEW.anxious_q11 + NEW.anxious_q12 +
        NEW.anxious_q13 + NEW.anxious_q14 + NEW.anxious_q15 + NEW.anxious_q16 +
        NEW.anxious_q17 + NEW.anxious_q18
    ) / 18.0;

    NEW.avoidant_score := (
        NEW.avoidant_q1 + NEW.avoidant_q2 + NEW.avoidant_q3 + NEW.avoidant_q4 +
        NEW.avoidant_q5 + NEW.avoidant_q6 + NEW.avoidant_q7 + NEW.avoidant_q8 +
        NEW.avoidant_q9 + NEW.avoidant_q10 + NEW.avoidant_q11 + NEW.avoidant_q12 +
        NEW.avoidant_q13 + NEW.avoidant_q14 + NEW.avoidant_q15 + NEW.avoidant_q16 +
        NEW.avoidant_q17 + NEW.avoidant_q18
    ) / 18.0;

    -- Calculate the secure score based on the new averages
    NEW.secure_score := 4 + (((4 - NEW.anxious_score) + (4 - NEW.avoidant_score)) / 2.0);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calculate_others_attachment_scores()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculate average scores for the new or updated row
    NEW.anxious_score := (
        NEW.anxious_q1 + NEW.anxious_q2 + NEW.anxious_q3 + NEW.anxious_q4 +
        NEW.anxious_q5 + NEW.anxious_q6 + NEW.anxious_q7 + NEW.anxious_q8 +
        NEW.anxious_q9 + NEW.anxious_q10 + NEW.anxious_q11
    ) / 11.0;

    NEW.avoidant_score := (
        NEW.avoidant_q1 + NEW.avoidant_q2 + NEW.avoidant_q3 + NEW.avoidant_q4 +
        NEW.avoidant_q5 + NEW.avoidant_q6 + NEW.avoidant_q7 + NEW.avoidant_q8 +
        NEW.avoidant_q9 + NEW.avoidant_q10 + NEW.avoidant_q11
    ) / 11.0;

    NEW.secure_score := (
        NEW.secure_q1 + NEW.secure_q2 + NEW.secure_q3 + NEW.secure_q4 +
        NEW.secure_q5 + NEW.secure_q6 + NEW.secure_q7 + NEW.secure_q8 +
        NEW.secure_q9 + NEW.secure_q10 + NEW.secure_q11
    ) / 11.0;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



DROP TRIGGER IF EXISTS trg_assess_yourself_scores ON assess_yourself;
DROP TRIGGER IF EXISTS trg_assess_others_scores ON assess_others;

CREATE TRIGGER trg_assess_yourself_scores
BEFORE INSERT OR UPDATE ON assess_yourself
FOR EACH ROW
EXECUTE FUNCTION calculate_you_attachment_scores();

CREATE TRIGGER trg_assess_others_scores
BEFORE INSERT OR UPDATE ON assess_others
FOR EACH ROW
EXECUTE FUNCTION calculate_others_attachment_scores();

