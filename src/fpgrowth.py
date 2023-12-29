from pyspark.ml.fpm import FPGrowth
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# 设置SparkSession的master参数为yarn
spark = SparkSession.builder.appName("FPGrowth").master("yarn").getOrCreate()

data = spark.read.text("/user/root/input/data_hanlp")
transactions = data.rdd.map(lambda line: (line.value.strip().split(' '),)).toDF(["items",])

fpGrowth = FPGrowth(itemsCol="items", minSupport=4e-6, minConfidence=0.4)
model = fpGrowth.fit(transactions)

answer = model.associationRules

def str_to_arr(my_list):
    my_list.sort()
    return  '+'.join([str(elem) for elem in my_list])

str_to_arr_udf = udf(str_to_arr, StringType())
answer = answer.withColumn("antecedent", str_to_arr_udf(answer["antecedent"]))
answer = answer.withColumn("consequent", str_to_arr_udf(answer["consequent"]))
answer.write.mode('overwrite').option("header",True).csv("/user/root/output/res_hanlp")

spark.stop()