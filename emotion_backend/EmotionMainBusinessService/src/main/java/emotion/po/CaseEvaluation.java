package emotion.po;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.util.Date;

@TableName("case_evaluation")
@Data
public class CaseEvaluation {
    @TableField("name")
    private String name;
    @TableField("staff_id")
    private Long staffId;
    @TableField("customer_phone")
    private String customerPhone;
    @TableField("create_date")
    private Date createDate;
    @TableField("case_score")
    private Double caseScore;
    @TableField("staff_emotion_score")
    private Double staffEmotionScore;
    @TableField("staff_polite_words_percent")
    private Double staffPoliteWordsPercent;
    @TableField("customer_emotion_score")
    private Double customerEmotionScore;
    @TableField("customer_satisfied_score")
    private Integer customerSatisfiedScore;
    @TableField("staff_understand_problem_score")
    private Integer staffUnderstandProblemScore;
    @TableField("staff_solve_problem_score")
    private Integer staffSolveProblemScore;
    @TableField("staff_pessimistic_num")
    private Integer staffPessimisticNum;
    @TableField("staff_optimistic_num")
    private Integer staffOptimisticNum;
    @TableField("customer_pessimistic_num")
    private Integer customerPessimisticNum;
    @TableField("customer_optimistic_num")
    private Integer customerOptimisticNum;
    @TableField("customer_satisfied")
    private String customerSatisfied;
    @TableField("staff_understand_problem")
    private String staffUnderstandProblem;
    @TableField("staff_solve_problem")
    private String staffSolveProblem;
    @TableField("time_in_seconds")
    private Double timeInSeconds;
    @TableField("speech_words_per_min")
    private Double speechWordsPerMin;
    @TableField("pronunciation_score")
    private Double pronunciationScore;
}
