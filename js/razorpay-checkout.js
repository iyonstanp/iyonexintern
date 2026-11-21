'use strict';

(() => {
  const form = document.getElementById('payment-form');
  if (!form) return;

  const button = document.getElementById('pay-button');
  const buttonLabel = document.getElementById('pay-button-label');
  const status = document.getElementById('payment-status');

  function showStatus(message, isError) {
    status.textContent = message;
    status.style.display = 'block';
    status.style.color = isError ? '#b42318' : 'var(--text-dim)';
  }

  function setBusy(busy, label) {
    button.disabled = busy;
    buttonLabel.textContent = label || (busy ? 'Connecting to Razorpay…' : 'Continue to secure payment');
    button.style.opacity = busy ? '0.7' : '1';
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    if (!window.Razorpay) {
      showStatus('The secure checkout could not load. Refresh this page or contact IYONEX.', true);
      return;
    }

    const rupees = Number(document.getElementById('payment-amount').value);
    const amountPaise = Math.round(rupees * 100);
    if (!Number.isSafeInteger(amountPaise) || amountPaise < 100 || amountPaise > 100000000) {
      showStatus('Enter an amount between ₹1.00 and ₹10,00,000.00.', true);
      return;
    }

    const payer = {
      name: document.getElementById('payer-name').value.trim(),
      email: document.getElementById('payer-email').value.trim(),
      reference: document.getElementById('payment-reference').value.trim(),
      amount: amountPaise
    };

    setBusy(true, 'Creating secure order…');
    showStatus('Connecting securely to Razorpay. Do not refresh this page.', false);

    try {
      const orderResponse = await fetch('/api/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payer)
      });
      const order = await orderResponse.json();
      if (!orderResponse.ok) throw new Error(order.error || 'Could not create a payment order.');

      const options = {
        key: order.key_id,
        amount: order.amount,
        currency: order.currency,
        name: 'IYONEX Automation Private Limited',
        description: 'Invoice / confirmed programme fee',
        order_id: order.order_id,
        prefill: { name: payer.name, email: payer.email },
        notes: { reference: payer.reference },
        theme: { color: '#2563eb' },
        handler: async function (response) {
          setBusy(true, 'Verifying payment…');
          showStatus('Payment response received. Verifying it with IYONEX and Razorpay…', false);
          try {
            const verifyResponse = await fetch('/api/verify-payment', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(response)
            });
            const result = await verifyResponse.json();

            if (result.paid === true && result.verified === true) {
              showStatus(
                'Payment captured and verified. Reference: ' + payer.reference +
                '. Razorpay payment ID: ' + result.payment_id +
                '. Please retain this confirmation for your records.',
                false
              );
              form.reset();
            } else if (result.verified === true) {
              showStatus(
                'The payment signature is valid, but the payment is not yet captured by Razorpay. Status: ' +
                (result.payment_status || 'pending') +
                '. Please do not pay again. Contact IYONEX with your reference: ' + payer.reference,
                false
              );
            } else {
              throw new Error(result.error || 'Payment verification failed. Do not retry until IYONEX checks the payment.');
            }
          } catch (error) {
            showStatus(error.message || 'Payment verification could not be completed. Do not pay again; contact IYONEX with your invoice reference.', true);
          } finally {
            setBusy(false);
          }
        },
        modal: {
          ondismiss: function () {
            setBusy(false);
            showStatus('Checkout was closed. No payment confirmation was received. You can try again using the same invoice details.', false);
          }
        }
      };

      const checkout = new window.Razorpay(options);
      checkout.on('payment.failed', function (failure) {
        setBusy(false);
        const reason = failure && failure.error && failure.error.description
          ? failure.error.description
          : 'The payment could not be completed.';
        showStatus(reason + ' No successful payment was confirmed. Check your Razorpay payment status before trying again.', true);
      });
      checkout.open();
      setBusy(false, 'Secure checkout opened');
    } catch (error) {
      setBusy(false);
      showStatus(error.message || 'Unable to start checkout. Please try again or contact IYONEX.', true);
    }
  });
})();
