package emotion.po;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.util.Date;

@TableName("staff_evaluation")
@Data
public class StaffEvaluation {
    @TableId(value = "id", type = IdType.AUTO)
    private Long id;
    @TableField("staff_id")
    private Long staffId;
    @TableField("create_date")
    private Date createDate;
    @TableField("score")
    private Double score;
    @TableField("service_num")
    private Integer serviceNum;
    @TableField("service_num_score")
    private Double serviceNumScore;
    @TableField("problem_solve_score")
    private Double problemSolveScore;
    @TableField("problem_unsolved_percent")
    private Double problemUnsolvedPercent;
    @TableField("problem_solve")
    private String problemSolve;
    @TableField("average_time")
    private Double averageTime;
    @TableField("time_score")
    private Double timeScore;
    @TableField("average_time_description")
    private String averageTimeDescription;
    @TableField("staff_emotion_score")
    private Double staffEmotionScore;
    @TableField("staff_pessimistic_num")
    private Integer staffPessimisticNum;
    @TableField("staff_optimistic_num")
    private Integer staffOptimisticNum;
    @TableField("staff_pessimistic_percent")
    private Double staffPessimisticPercent;
    @TableField("staff_optimistic_percent")
    private Double staffOptimisticPercent;
    @TableField("staff_emotion_control_ability")
    private String staffEmotionControlAbility;
    @TableField("customer_emotion_score")
    private Double customerEmotionScore;
    @TableField("customer_pessimistic_num")
    private Integer customerPessimisticNum;
    @TableField("customer_optimistic_num")
    private Integer customerOptimisticNum;
    @TableField("customer_pessimistic_percent")
    private Double customerPessimisticPercent;
    @TableField("customer_optimistic_percent")
    private Double customerOptimisticPercent;
    @TableField("customer_emotion_control_ability")
    private String customerEmotionControlAbility;
    @TableField("polite_words_score")
    private Double politeWordsScore;
    @TableField("polite_words_usage")
    private String politeWordsUsage;
    @TableField("speech_speed_score")
    private Double speechSpeedScore;
    @TableField("average_speech_speed")
    private Double averageSpeechSpeed;
    @TableField("speech_speed")
    private String speechSpeed;
    @TableField("average_pronunciation_score")
    private Double averagePronunciationScore;
    @TableField("average_case_score")
    private Double averageCaseScore;
    @TableField("growth_score")
    private Double growthScore;
    @TableField("short_term_growth_trend")
    private String shortTermGrowthTrend;
    @TableField("long_term_growth_trend")
    private String longTermGrowthTrend;
}
