# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:55:09 2025

@author: DELL
"""
import json
import pandas as pd

dosya_yolu = "D:/2025-06-09T21_05_10Z-P_ATS_INVENTORY_COMPANY_CUSTOMER-d4444380-8055-4d33-aaba-204e9088fc4a.json"

with open(dosya_yolu, "r", encoding="utf-8-sig") as dosya:
    veri = json.load(dosya)

activities = veri.get("value", [])

veri_listesi = []

for activity in activities:
    kayit = {}

    # Temel alanlar
    kayit["activityName"] = activity.get('activityName')
    kayit["activityRunEnd"] = activity.get('activityRunEnd')
    kayit["activityRunId"] = activity.get('activityRunId')
    kayit["activityRunStart"] = activity.get('activityRunStart')
    kayit["activityType"] = activity.get('activityType')
    kayit["durationInMs"] = activity.get('durationInMs')
    kayit["pipelineName"] = activity.get('pipelineName')
    kayit["pipelineRunId"] = activity.get('pipelineRunId')
    kayit["recoveryStatus"] = activity.get('recoveryStatus')
    kayit["retryAttempt"] = activity.get('retryAttempt')
    kayit["status"] = activity.get('status')

    # Billing Reference
    billing = activity.get("output", {}).get("billingReference", {})
    kayit["billingActivityType"] = billing.get("activityType")
    # billableDuration ve totalBillableDuration listeler, onları string yapabiliriz
    bd_list = billing.get("billableDuration", [])
    tb_list = billing.get("totalBillableDuration", [])
    kayit["billableDuration"] = str(bd_list) if bd_list else None
    kayit["totalBillableDuration"] = str(tb_list) if tb_list else None

    # Output
    output = activity.get("output", {})
    kayit["copyDuration"] = output.get("copyDuration")
    kayit["dataConsistencyVerification"] = output.get("dataConsistencyVerification", {}).get("VerificationResult") if output.get("dataConsistencyVerification") else None
    kayit["dataRead"] = output.get("dataRead")
    kayit["dataWritten"] = output.get("dataWritten")
    kayit["durationInQueue"] = output.get("durationInQueue", {}).get("integrationRuntimeQueue") if output.get("durationInQueue") else None
    kayit["effectiveIntegrationRuntime"] = output.get("effectiveIntegrationRuntime")

    # Execution Details -> Bu liste olabilir, ilk elemanı alabiliriz ya da string yapabiliriz
    execution_details = output.get("executionDetails", [])
    if execution_details:
        detail = execution_details[0]
        durations = detail.get("detailedDurations", {})
        profile_queue = detail.get("profile", {}).get("queue", {})
        kayit["queuingDuration"] = durations.get("queuingDuration")
        kayit["timeToFirstByte"] = durations.get("timeToFirstByte")
        kayit["transferDuration"] = durations.get("transferDuration")
        kayit["totalDuration"] = detail.get("duration")
        kayit["interimDataWritten"] = detail.get("interimDataWritten")
        kayit["interimRowsCopied"] = detail.get("interimRowsCopied")
        kayit["queueStatus"] = profile_queue.get("status")
        kayit["queueDuration"] = profile_queue.get("duration")
    else:
        # Eğer yoksa boş bırak
        for key in ["queuingDuration", "timeToFirstByte", "transferDuration", "totalDuration",
                    "interimDataWritten", "interimRowsCopied", "queueStatus", "queueDuration"]:
            kayit[key] = None

    # ROW bilgileri
    kayit["rowActivity"] = output.get("activityName")  # Çoğunlukla aynı activityName
    kayit["rowsCopied"] = output.get("rowsCopied")
    kayit["rowsRead"] = output.get("rowsRead")
    kayit["sinkPeakConnections"] = output.get("sinkPeakConnections")
    kayit["sourcePeakConnections"] = output.get("sourcePeakConnections")
    kayit["sqlDwPolyBase"] = output.get("sqlDwPolyBase")
    kayit["throughput"] = output.get("throughput")
    kayit["usedParallelCopies"] = output.get("usedParallelCopies")

    veri_listesi.append(kayit)

# DataFrame oluştur
df = pd.DataFrame(veri_listesi)

# Excel'e kaydet
df.to_excel(r"C:\Users\DELL\OneDrive\Masaüstü\dosya1.xlsx", index=False)
print("Excel dosyası oluşturuldu.")







    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    