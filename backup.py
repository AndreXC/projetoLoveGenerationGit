# match objectResultProduto.status:
            #     case 'approved':
            #         InstanceCompraCliente.status_compra = "approved"
            #         InstanceCompraCliente.clienteId =  payment_id
            #         InstanceCompraCliente.save()
            #         instancePosPayment : createEstruturaProject =  createEstruturaProject(InstanceCompraCliente.token_referencia)
            #         result, StrErr = instancePosPayment.__createMensagem__()
            #         if not result and StrErr != '':
            #             instancepaymentNotProcess: paymentNotProcess = paymentNotProcess(
            #                 token_referencia=InstanceCompraCliente.token_referencia,
            #                 status_compra=InstanceCompraCliente.status_compra,
            #                 clienteId=InstanceCompraCliente.clienteId,
            #                 details='Erro: ' + str(StrErr)
            #             )
            #             instancepaymentNotProcess.save()
            #             return JsonResponse({"status": "failed"}, status=400)
            #     case 'pending':
            #         InstanceCompraCliente.status_compra = "pending" 
            #         InstanceCompraCliente.save()

            #         JsonMensagem:dict = json.loads(InstanceCompraCliente.dados_requisicao.replace("'", "\""))
            #         instancePaymentPending:PaymentPending = PaymentPending(email=JsonMensagem['email'], qrcode=objectResultProduto.qr_code, name=objectResultProduto.name, external_reference=InstanceCompraCliente.token_referencia)
            #         result, StrErr = instancePaymentPending.__SendEmail__()
            #         if not result and StrErr !='':
            #             instanceError: Error = Error(
            #                     error_type= 'PaymentPendingClass',
            #                     details=StrErr
            #                 )
            #             instanceError.save()

            #     case 'rejected':
            #         InstanceCompraCliente.status_compra = 'rejected' 
            #         InstanceCompraCliente.save()

            #         JsonMensagem: json = json.loads(InstanceCompraCliente.dados_requisicao.replace("'", "\""))
            #         instanceSaveTblob: SaveArquivosBlob = SaveArquivosBlob()
            #         result, StrErr = instanceSaveTblob.__extractArqAll__(JsonMensagem['idfotosSalvas'])
            #         if not result and StrErr !='':
            #             instanceError: Error = Error(
            #                     error_type= 'instanceSaveTblob.__extractArqAll__',
            #                     details=StrErr
            #                 )
            #             instanceError.save()
    